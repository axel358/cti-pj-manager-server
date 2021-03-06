from django.urls import path, include
from rest_framework import routers

from .views import (
    RegisterView,
    ChangePasswordView,
    UpdateProfileView,
    LogoutAllView, UsersListView
)
from .viewsets import ProgramViewSet, ProjectViewSet, MembersViewSet, ProjectDocumentViewSet
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"programs", ProgramViewSet)
router.register(r"members", MembersViewSet)
router.register(r"projectdocuments", ProjectDocumentViewSet)
app_name = "server"

urlpatterns = [
    path("", include(router.urls)),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="user_register"),
    path(
        "change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="user_change_password",
    ),
    path(
        "update_profile/<int:pk>/",
        UpdateProfileView.as_view(),
        name="auth_update_profile",
    ),
    path(
        "users_list/",
        UsersListView.as_view(),
        name="list_users",
    ),
    path("logout/", LogoutAllView.as_view(), name="user_logout"),

]
