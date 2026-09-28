import requests
from datetime import datetime, timezone

from mongo import db


FASTAPI_ACTIVITY_URL = (
    "http://127.0.0.1:8000/api/v1/activities/"
)


def sync_activity_to_mongodb():

    response = requests.get(
        FASTAPI_ACTIVITY_URL,
        timeout=120
    )

    if response.status_code != 200:

        print(
            "FastAPI error:",
            response.status_code,
            response.text
        )

        return None

    records = response.json()

    print(
        f"Fetched {len(records)} activity records"
    )

    if not records:
        return {
            "total_fetched": 0,
            "total_processed": 0
        }

    # --------------------------------------------------
    # Basic video information
    # --------------------------------------------------

    first_record = records[0]

    video_name = first_record.get("video_name")

    # --------------------------------------------------
    # Calculate unique persons
    # --------------------------------------------------

    person_ids = set()

    for record in records:

        person_id = record.get("person_id")

        if person_id is not None:
            person_ids.add(person_id)

    total_unique_persons = len(person_ids)

    # --------------------------------------------------
    # Calculate activity summary
    # --------------------------------------------------

    walking_count = 0
    standing_count = 0
    sitting_count = 0

    for record in records:

        activity = (
            record.get("activity", "")
            .strip()
            .lower()
        )

        if activity == "walking":
            walking_count += 1

        elif activity == "standing":
            standing_count += 1

        elif activity == "sitting":
            sitting_count += 1

    # --------------------------------------------------
    # Build persons array
    # --------------------------------------------------

    persons_map = {}

    for record in records:

        person_id = record.get("person_id")

        if person_id is None:
            continue

        if person_id not in persons_map:

            persons_map[person_id] = {
                "person_id": person_id,
                "activities": []
            }

        persons_map[person_id]["activities"].append({
            "activity": record.get("activity"),
            "start_time": record.get("start_time"),
            "end_time": record.get("end_time"),
            "duration_seconds": record.get(
                "duration_seconds"
            )
        })

    persons = list(persons_map.values())

    # --------------------------------------------------
    # Get video duration
    # --------------------------------------------------

    video_duration_seconds = 0

    for record in records:

        end_time = record.get("end_time")

        if end_time:

            try:

                parts = end_time.split(":")

                if len(parts) == 3:

                    hours = float(parts[0])
                    minutes = float(parts[1])
                    seconds = float(parts[2])

                    total_seconds = (
                        hours * 3600
                        + minutes * 60
                        + seconds
                    )

                else:

                    total_seconds = float(end_time)

                if total_seconds > video_duration_seconds:
                    video_duration_seconds = total_seconds

            except (ValueError, AttributeError):
                pass

    # --------------------------------------------------
    # PostgreSQL created time
    # --------------------------------------------------

    postgres_created_at = None

    created_values = [
        record.get("created_at")
        for record in records
        if record.get("created_at")
    ]

    if created_values:

        postgres_created_at = min(
            created_values
        )

    # --------------------------------------------------
    # Final MongoDB document
    # --------------------------------------------------

    mongo_document = {

        "video_name": video_name,

        "video_duration_seconds": round(
            video_duration_seconds,
            2
        ),

        "summary": {

            "total_unique_persons":
                total_unique_persons,

            "walking":
                walking_count,

            "standing":
                standing_count,

            "sitting":
                sitting_count
        },

        "persons": persons,

        "postgres_created_at":
            postgres_created_at,

        "synced_at":
            datetime.now(timezone.utc)
    }

    # --------------------------------------------------
    # Save to MongoDB
    # --------------------------------------------------

    collection = db["activity data"]

    result = collection.update_one(
        {
            "video_name": video_name
        },
        {
            "$set": mongo_document
        },
        upsert=True
    )

    print()
    print(
        "Activity data saved to MongoDB"
    )

    print(
        "Video:",
        video_name
    )

    print(
        "Total unique persons:",
        total_unique_persons
    )

    print(
        "Walking:",
        walking_count
    )

    print(
        "Standing:",
        standing_count
    )

    print(
        "Sitting:",
        sitting_count
    )

    return {
        "total_fetched": len(records),
        "total_processed": 1
    }