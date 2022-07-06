from django.urls import path
from .views import (
    RegisterView,
    ChangePasswordView,
    UpdateProfileView,
    LogoutAllView,
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

urlpatterns = [
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
    path("logout/", LogoutAllView.as_view(), name="user_logout"),

]
