import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_URL = "http://127.0.0.1:8001/api/token/"
SYNC_URL = "http://127.0.0.1:8001/api/common/"

USERNAME = os.getenv("DJANGO_USERNAME")
PASSWORD = os.getenv("DJANGO_PASSWORD")


def get_access_token():
    response = requests.post(
        TOKEN_URL,
        json={
            "username": USERNAME,
            "password": PASSWORD
        }
    )

    if response.status_code == 200:
        return response.json()["access"]

    print("Token error:", response.text)
    return None


def sync_data():
    access_token = get_access_token()

    if not access_token:
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        SYNC_URL,
        headers=headers
    )

    print("Status:", response.status_code)
    print("Response:", response.text)


while True:
    sync_data()
    print("Waiting 2 minutes...")
    time.sleep(120)