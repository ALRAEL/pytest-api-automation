import os
import time
import requests
import pytest
from dotenv import load_dotenv
import logging

logging.basicConfig(
    filename='test_api.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
load_dotenv()

TOKEN = os.getenv("GOREST_TOKEN")
if not TOKEN:
    raise Exception("GOREST_TOKEN tidak ditemukan. Pastikan sudah ada di file .env!")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

BASE_URL_USERS = "https://gorest.co.in/public/v2/users"
BASE_URL_POSTS = "https://gorest.co.in/public/v2/posts"
BASE_URL_COMMENTS = "https://gorest.co.in/public/v2/comments"
BASE_URL_TODOS = "https://gorest.co.in/public/v2/todos"

# Global variables to store created resource IDs
user_id = None
post_id = None
comment_id = None
todo_id = None

def test_create_user():
    global user_id
    unique_email = f"auto_test_{int(time.time())}@example.com"
    payload = {
        "name": "Auto Test User",
        "email": unique_email,
        "gender": "male",
        "status": "active"
    }
    response = requests.post(BASE_URL_USERS, json=payload, headers=HEADERS)
    logging.info(f"Create user response: {response.json()}")
    assert response.status_code == 201
    user_id = response.json()["id"]

def test_get_user():
    global user_id
    response = requests.get(f"{BASE_URL_USERS}/{user_id}", headers=HEADERS)
    logging.info(f"Get user response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

def test_create_post():
    global user_id, post_id
    payload = {
        "user_id": user_id,
        "title": "Test Post Title",
        "body": "This is a test post body."
    }
    response = requests.post(BASE_URL_POSTS, json=payload, headers=HEADERS)
    logging.info(f"Create post response: {response.json()}")
    assert response.status_code == 201
    post_id = response.json()["id"]

def test_get_post():
    global post_id
    response = requests.get(f"{BASE_URL_POSTS}/{post_id}", headers=HEADERS)
    logging.info(f"Get post response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["id"] == post_id

def test_create_comment():
    global post_id, comment_id
    payload = {
        "post_id": post_id,
        "name": "Test Commenter",
        "email": "commenter@example.com",
        "body": "This is a test comment."
    }
    response = requests.post(BASE_URL_COMMENTS, json=payload, headers=HEADERS)
    logging.info(f"Create comment response: {response.json()}")
    assert response.status_code == 201
    comment_id = response.json()["id"]

def test_update_comment():
    global comment_id
    payload = {
        "name": "Updated Commenter",
        "body": "This comment has been updated."
    }
    response = requests.put(f"{BASE_URL_COMMENTS}/{comment_id}", json=payload, headers=HEADERS)
    logging.info(f"Update comment response: {response.json()}")
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Commenter"

def test_create_todo():
    global user_id, todo_id
    payload = {
        "user_id": user_id,
        "title": "Test Todo Item",
        "due_on": "2025-12-31T23:59:59.000+05:30",
        "status": "pending"
    }
    response = requests.post(BASE_URL_TODOS, json=payload, headers=HEADERS)
    logging.info(f"Create todo response: {response.json()}")
    assert response.status_code == 201
    todo_id = response.json()["id"]

def test_delete_todo():
    global todo_id
    response = requests.delete(f"{BASE_URL_TODOS}/{todo_id}", headers=HEADERS)
    logging.info(f"Delete todo response status code: {response.status_code}")
    assert response.status_code == 204

def test_delete_user():
    global user_id
    response = requests.delete(f"{BASE_URL_USERS}/{user_id}", headers=HEADERS)
    logging.info(f"Delete user response status code: {response.status_code}")
    assert response.status_code == 204

