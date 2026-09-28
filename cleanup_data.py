import os
import time
import requests
from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv
from mongo import db


load_dotenv()


TOKEN_URL = "http://127.0.0.1:8001/api/token/"
FASTAPI_DELETE_URL = "http://127.0.0.1:8000/api/v1/detections"

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


def cleanup_synced_data():

    access_token = get_access_token()

    if not access_token:
        return

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    collection = db["postgreSQL synced data"]

    two_hours_ago = (
        datetime.now(timezone.utc) - timedelta(hours=2)
    )

    records = collection.find({
        "synced_at": {
            "$lte": two_hours_ago
        }
    })

    deleted_count = 0

    for record in records:

        postgres_id = record.get("postgres_id")

        if postgres_id is None:
            continue

        url = f"{FASTAPI_DELETE_URL}/{postgres_id}"

        response = requests.delete(
            url,
            headers=headers
        )

        if response.status_code == 200:
            print(
                f"PostgreSQL record {postgres_id} "
                f"deleted successfully"
            )

            deleted_count += 1

        elif response.status_code == 404:
            print(
                f"PostgreSQL record {postgres_id} "
                f"already deleted"
            )

        else:
            print(
                f"Failed to delete PostgreSQL record "
                f"{postgres_id}: {response.status_code}"
            )

    print(
        f"Total PostgreSQL records deleted: {deleted_count}"
    )


if __name__ == "__main__":

    while True:
        cleanup_synced_data()

        print("Waiting 2 hours...")

        time.sleep(7200)