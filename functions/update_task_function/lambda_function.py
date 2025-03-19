import json
import uuid
from db import get_db
from models import get_task_collection
import logging
from bson import ObjectId

def update_task(event, context):
    db = get_db()
    task_collection = get_task_collection(db)

    try:
        task_id = event["pathParameters"]["id"]
        body = json.loads(event["body"])
        new_status = body["status"]

        result = task_collection.update_one({"id": task_id}, {"$set": {"status": new_status}})

        if result.matched_count == 0:
            return {"statusCode": 404, "body": json.dumps({"message": "Task not found"})}

        return {"statusCode": 200, "body": json.dumps({"message": "Task updated"})}

    except Exception as e:
        logging.error(f"Error in create_task: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
