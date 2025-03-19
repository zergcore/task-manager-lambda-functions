import json
import uuid
from db import get_db
from models import get_task_collection
import logging
from bson import ObjectId

def lambda_handler(event, context):
    db = get_db()
    task_collection = get_task_collection(db)

    try:
        tasks = list(task_collection.find({}, {"_id": 0}))  # Exclude MongoDB's default _id field
        return {"statusCode": 200, "body": json.dumps(tasks)}

    except Exception as e:
        logging.error(f"Error in create_task: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    db = get_db()
    task_collection = get_task_collection(db)

    try:
        task_id = event["pathParameters"]["id"]
        result = task_collection.delete_one({"id": task_id})

        if result.deleted_count == 0:
            return {"statusCode": 404, "body": json.dumps({"message": "Task not found"})}

        return {"statusCode": 200, "body": json.dumps({"message": "Task deleted"})}

    except Exception as e:
        logging.error(f"Error in create_task: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }