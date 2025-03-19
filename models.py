from pymongo import ASCENDING

def get_task_collection(db):
    task_collection = db.tasks
    task_collection.create_index([("id", ASCENDING)], unique=True)  # Ensure unique task IDs
    return task_collection
