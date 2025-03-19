import json
import os
import jwt

def verify_token(event):
    SECRET_KEY = os.getenv("JWT_SECRET")
    auth_header = event.get("headers", {}).get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return {"statusCode": 401, "body": json.dumps({"message": "Unauthorized"})}

    token = auth_header.split(" ")[1]

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded  # Returns user info

    except jwt.ExpiredSignatureError:
        return {"statusCode": 403, "body": json.dumps({"message": "Token expired"})}

    except jwt.InvalidTokenError:
        return {"statusCode": 403, "body": json.dumps({"message": "Invalid token"})}
