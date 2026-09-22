from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bson import ObjectId
import json

from mongo import students_collection


@csrf_exempt
def students(request):

    # CREATE
    if request.method == "POST":
        data = json.loads(request.body)

        result = students_collection.insert_one(data)

        return JsonResponse({
            "message": "Student created successfully",
            "id": str(result.inserted_id)
        }, status=201)

    # READ
    if request.method == "GET":
        students_list = list(students_collection.find())

        for student in students_list:
            student["_id"] = str(student["_id"])

        return JsonResponse(students_list, safe=False)

    return JsonResponse({
        "message": "Method not allowed"
    }, status=405)


@csrf_exempt
def student_detail(request, student_id):

    try:
        object_id = ObjectId(student_id)
    except Exception:
        return JsonResponse({
            "message": "Invalid student ID"
        }, status=400)

    # READ ONE
    if request.method == "GET":
        student = students_collection.find_one({
            "_id": object_id
        })

        if student is None:
            return JsonResponse({
                "message": "Student not found"
            }, status=404)

        student["_id"] = str(student["_id"])

        return JsonResponse(student)

    # UPDATE
    if request.method == "PUT":
        data = json.loads(request.body)

        result = students_collection.update_one(
            {"_id": object_id},
            {"$set": data}
        )

        if result.matched_count == 0:
            return JsonResponse({
                "message": "Student not found"
            }, status=404)

        return JsonResponse({
            "message": "Student updated successfully"
        })

    # DELETE
    if request.method == "DELETE":
        result = students_collection.delete_one({
            "_id": object_id
        })

        if result.deleted_count == 0:
            return JsonResponse({
                "message": "Student not found"
            }, status=404)

        return JsonResponse({
            "message": "Student deleted successfully"
        })

    return JsonResponse({
        "message": "Method not allowed"
    }, status=405)