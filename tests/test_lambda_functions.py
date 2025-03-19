# import pytest
# import json
# from lambda_functions import create_task

# def test_create_task():
#     event = {
#         "body": json.dumps({"title": "Test Task", "description": "This is a test"})
#     }
#     response = create_task(event, None)
#     assert response["statusCode"] == 201

import pytest
import json
from unittest.mock import patch, MagicMock
from lambda_functions import create_task, get_tasks, update_task, delete_task

@pytest.fixture
def mock_db():
    with patch("lambda_functions.get_db") as mock_get_db:
        mock_db = MagicMock()
        mock_get_db.return_value = mock_db
        yield mock_db

@pytest.fixture
def mock_task_collection():
    with patch("lambda_functions.get_task_collection") as mock_get_collection:
        mock_collection = MagicMock()
        mock_get_collection.return_value = mock_collection
        yield mock_collection

def test_create_task_success(mock_db, mock_task_collection):
    event = {
        "body": json.dumps({"title": "Test Task", "description": "Test Description"})
    }
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = "some_id"
    mock_task_collection.insert_one.return_value = mock_insert_result

    response = create_task(event, None)

    assert response["statusCode"] == 201
    body = json.loads(response["body"])
    assert body["message"] == "Task created"
    assert body["task_id"] == "some_id"
    mock_task_collection.insert_one.assert_called_once()

def test_create_task_missing_fields(mock_db, mock_task_collection):
    event = {
        "body": json.dumps({"title": "Test Task"})
    }

    response = create_task(event, None)

    assert response["statusCode"] == 400
    body = json.loads(response["body"])
    assert body["error"] == "Missing title or description"
    mock_task_collection.insert_one.assert_not_called()

def test_create_task_exception(mock_db, mock_task_collection):
    event = {
        "body": json.dumps({"title": "Test Task", "description": "Test Description"})
    }
    mock_task_collection.insert_one.side_effect = Exception("DB Error")

    response = create_task(event, None)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "DB Error" in body["error"]

def test_get_tasks_success(mock_db, mock_task_collection):
    mock_task_collection.find.return_value = [
        {"title": "Task 1", "description": "Desc 1", "status": "to do"},
        {"title": "Task 2", "description": "Desc 2", "status": "done"}
    ]

    response = get_tasks({}, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert len(body) == 2
    mock_task_collection.find.assert_called_once_with({}, {"_id": 0})

def test_get_tasks_exception(mock_db, mock_task_collection):
    mock_task_collection.find.side_effect = Exception("DB Error")

    response = get_tasks({}, None)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "DB Error" in body["error"]

def test_update_task_success(mock_db, mock_task_collection):
    event = {
        "pathParameters": {"id": "task123"},
        "body": json.dumps({"status": "done"})
    }
    mock_update_result = MagicMock()
    mock_update_result.matched_count = 1
    mock_task_collection.update_one.return_value = mock_update_result

    response = update_task(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Task updated"
    mock_task_collection.update_one.assert_called_once_with(
        {"id": "task123"}, {"$set": {"status": "done"}}
    )

def test_update_task_not_found(mock_db, mock_task_collection):
    event = {
        "pathParameters": {"id": "nonexistent"},
        "body": json.dumps({"status": "done"})
    }
    mock_update_result = MagicMock()
    mock_update_result.matched_count = 0
    mock_task_collection.update_one.return_value = mock_update_result

    response = update_task(event, None)

    assert response["statusCode"] == 404
    body = json.loads(response["body"])
    assert body["message"] == "Task not found"

def test_update_task_exception(mock_db, mock_task_collection):
    event = {
        "pathParameters": {"id": "task123"},
        "body": json.dumps({"status": "done"})
    }
    mock_task_collection.update_one.side_effect = Exception("DB Error")

    response = update_task(event, None)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "DB Error" in body["error"]

def test_delete_task_success(mock_db, mock_task_collection):
    event = {
        "pathParameters": {"id": "task123"}
    }
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 1
    mock_task_collection.delete_one.return_value = mock_delete_result

    response = delete_task(event, None)

    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert body["message"] == "Task deleted"
    mock_task_collection.delete_one.assert_called_once_with({"id": "task123"})

def test_delete_task_not_found(mock_db, mock_task_collection):
    event = {
        "pathParameters": {"id": "nonexistent"}
    }
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 0
    mock_task_collection.delete_one.return_value = mock_delete_result

    response = delete_task(event, None)

    assert response["statusCode"] == 404
    body = json.loads(response["body"])
    assert body["message"] == "Task not found"

def test_delete_task_exception(mock_db, mock_task_collection):
    event = {
        "pathParameters": {"id": "task123"}
    }
    mock_task_collection.delete_one.side_effect = Exception("DB Error")

    response = delete_task(event, None)

    assert response["statusCode"] == 500
    body = json.loads(response["body"])
    assert "DB Error" in body["error"]
