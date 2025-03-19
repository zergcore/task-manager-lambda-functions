import json
import uuid
from db import get_db
from models import get_task_collection
import logging
from bson import ObjectId

def create_task(event, context):
    db = get_db()
    task_collection = get_task_collection(db)

    try:
        body = json.loads(event.get("body", "{}"))
        title = body.get("title")
        description = body.get("description")

        if not title or not description:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing title or description"})
            }
        new_task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": description,
            "status": "to do"
        }

        result = task_collection.insert_one(new_task)

        return {
            "statusCode": 201,
            "body": json.dumps({
                "message": "Task created",
                "task_id": str(result.inserted_id)
            })
        }

    except Exception as e:
        logging.error(f"Error in create_task: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

def get_tasks(event, context):
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

def delete_task(event, context):
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