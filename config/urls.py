from django.contrib import admin
from django.urls import path

from college.views import (
    students,
    student_detail,
    protected_api,
    common_api,
    activity_common_api,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    # Student APIs
    path(
        "api/students/",
        students
    ),

    path(
        "api/students/<str:student_id>/",
        student_detail
    ),

    # JWT
    path(
        "api/token/",
        TokenObtainPairView.as_view()
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view()
    ),

    # Protected API
    path(
        "api/protected/",
        protected_api
    ),

    # ========================================================
    # VERSION 1
    # ========================================================

    path(
        "api/common/",
        common_api
    ),

    # ========================================================
    # VERSION 2
    # ========================================================

    path(
        "api/activity-common/",
        activity_common_api
    ),
]