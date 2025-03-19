import json
import bcrypt
import jwt
import os
from db import get_db

def lambda_handler(event, context):
    db = get_db
    users_collection = db["users"]

    SECRET_KEY = os.getenv("JWT_SECRET")
    body = json.loads(event["body"])
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return {"statusCode": 400, "body": json.dumps({"error": "Email and password required"})}

    user = users_collection.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return {"statusCode": 401, "body": json.dumps({"error": "Invalid credentials"})}

    # Generate JWT token
    token = jwt.encode({"email": email}, SECRET_KEY, algorithm="HS256")

    return {"statusCode": 200, "body": json.dumps({"token": token})}
