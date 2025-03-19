import json
import bcrypt
from db import get_db

def lambda_handler(event, context):
    db = get_db()
    users_collection = db["users"]

    body = json.loads(event["body"])
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return {"statusCode": 400, "body": json.dumps({"error": "Email and password required"})}

    # Check if user already exists
    if users_collection.find_one({"email": email}):
        return {"statusCode": 400, "body": json.dumps({"error": "User already exists"})}

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # Store user
    users_collection.insert_one({"email": email, "password": hashed_password})

    return {"statusCode": 201, "body": json.dumps({"message": "User registered successfully"})}
