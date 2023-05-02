from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Set up the MongoDB client and database
client = MongoClient("mongodb://localhost:27017/")
db = client["mydattabase"]
users_collection = db["mycoollection"]



# Route to get a list of all users
@app.route("/users", methods=["GET"])
def get_users():
    users = users_collection.find()
    user_list = []
    for user in users:
        user["_id"] = str(user["_id"])
        user_list.append(user)
    return jsonify(user_list)


# Route to get a user by ID
@app.route("/users/<string:user_id>", methods=["GET"])
def get_user(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    else:
        return jsonify({"message": "User not found."}), 404


# Route to create a new user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"]
    }
    result = users_collection.insert_one(new_user)
    return jsonify({"message": "User created.", "id": str(result.inserted_id)})


# Route to update an existing user
@app.route("/users/<string:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    updated_user = {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"]
    }
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": updated_user})
    if result.modified_count > 0:
        return jsonify({"message": "User updated."})
    else:
        return jsonify({"message": "User not found."}), 404


# Route to delete a user
@app.route("/users/<string:user_id>", methods=["DELETE"])
def delete_user(user_id):
    result = users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "User deleted."})
    else:
        return jsonify({"message": "User not found."}), 404


if __name__ == "__main__":
    app.run(debug=True)
