from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.students),
    path("students/<str:student_id>/", views.student_detail),
]