from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.students),
    path("students/<str:student_id>/", views.student_detail),

    # JWT protected API
    path("protected/", views.protected_api),

    # Common API
    path("common/", views.common_api),
]