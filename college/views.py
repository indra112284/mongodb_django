from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
import json

from mongo import students_collection

# Version 1
from .common_api import sync_postgres_to_mongodb

# Version 2
from .activity_common_api import sync_activity_to_mongodb

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


# ============================================================
# STUDENTS
# ============================================================

@csrf_exempt
def students(request):

    if request.method == "POST":

        data = json.loads(request.body)

        result = students_collection.insert_one(data)

        return JsonResponse(
            {
                "message": "Student created successfully",
                "id": str(result.inserted_id)
            },
            status=201
        )

    if request.method == "GET":

        students_list = list(
            students_collection.find()
        )

        for student in students_list:
            student["_id"] = str(student["_id"])

        return JsonResponse(
            students_list,
            safe=False
        )

    return JsonResponse(
        {
            "message": "Method not allowed"
        },
        status=405
    )


# ============================================================
# STUDENT DETAIL
# ============================================================

@csrf_exempt
def student_detail(request, student_id):

    try:
        object_id = ObjectId(student_id)

    except Exception:

        return JsonResponse(
            {
                "message": "Invalid student ID"
            },
            status=400
        )

    if request.method == "GET":

        student = students_collection.find_one(
            {
                "_id": object_id
            }
        )

        if student is None:

            return JsonResponse(
                {
                    "message": "Student not found"
                },
                status=404
            )

        student["_id"] = str(student["_id"])

        return JsonResponse(student)

    if request.method == "PUT":

        data = json.loads(request.body)

        result = students_collection.update_one(
            {
                "_id": object_id
            },
            {
                "$set": data
            }
        )

        if result.matched_count == 0:

            return JsonResponse(
                {
                    "message": "Student not found"
                },
                status=404
            )

        return JsonResponse(
            {
                "message": "Student updated successfully"
            }
        )

    if request.method == "DELETE":

        result = students_collection.delete_one(
            {
                "_id": object_id
            }
        )

        if result.deleted_count == 0:

            return JsonResponse(
                {
                    "message": "Student not found"
                },
                status=404
            )

        return JsonResponse(
            {
                "message": "Student deleted successfully"
            }
        )

    return JsonResponse(
        {
            "message": "Method not allowed"
        },
        status=405
    )


# ============================================================
# JWT PROTECTED API
# ============================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_api(request):

    return Response(
        {
            "message": "JWT authentication successful",
            "user": request.user.username
        }
    )


# ============================================================
# VERSION 1
# PostgreSQL Detection → MongoDB
# ============================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def common_api(request):

    result = sync_postgres_to_mongodb()

    if result is None:

        return Response(
            {
                "message": "Failed to sync data from FastAPI to MongoDB"
            },
            status=500
        )

    return Response(
        {
            "message": "Data fetched from PostgreSQL and saved to MongoDB",
            "total_fetched": result["total_fetched"],
            "total_processed": result["total_processed"]
        }
    )


# ============================================================
# VERSION 2
# PostgreSQL Activity → MongoDB
# ============================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def activity_common_api(request):

    result = sync_activity_to_mongodb()

    if result is None:

        return Response(
            {
                "message": "Failed to sync activity data"
            },
            status=500
        )

    return Response(
        {
            "message": "Activity data synced successfully",
            "total_fetched": result["total_fetched"],
            "total_processed": result["total_processed"]
        }
    )