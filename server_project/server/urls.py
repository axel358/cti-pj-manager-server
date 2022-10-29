from django.urls import path, include
from rest_framework import routers

from .views import (
    RegisterView,
    ChangePasswordView,
    UpdateUserView,
    UsersDeleteView,
    LogoutAllView, UsersListView, UserDetailsView
)
from .viewsets import ProgramViewSet, ProjectViewSet, MembersViewSet, ProjectDocumentViewSet, MyTokenVerifyView, \
    MyTokenObtainPairView, GroupDocumentViewSet, DocumentViewSet, DocumentGroupViewSet, ProgramDocumentViewSet, ProgramDocumentGroupViewSet, ProgramGroupDocumentViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"programs", ProgramViewSet)
router.register(r"members", MembersViewSet)
router.register(r"documents", DocumentViewSet)
router.register(r"projectdocuments", ProjectDocumentViewSet)
router.register(r"groupdocuments", GroupDocumentViewSet)
router.register(r"documentgroups", DocumentGroupViewSet)
router.register(r"programdocuments", ProjectDocumentViewSet)
router.register(r"programgroupdocuments", ProgramGroupDocumentViewSet)
router.register(r"programdocumentgroups", ProgramDocumentGroupViewSet)
app_name = "server"

urlpatterns = [
    path("", include(router.urls)),
    path("login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/verify/", MyTokenVerifyView.as_view(), name="token_verify"),
    path("register/", RegisterView.as_view(), name="user_register"),
    path(
        "change_password/<int:pk>/",
        ChangePasswordView.as_view(),
        name="user_change_password",
    ),
    path(
        "delete_user/<int:pk>/",
        UsersDeleteView.as_view(),
        name="delete_user",
    ),
    path(
        "update_user/<int:pk>/",
        UpdateUserView.as_view(),
        name="update_user",
    ),
    path(
        "users/",
        UsersListView.as_view(),
        name="list_users",
    ),
    path(
        "user/<int:pk>/",
        UserDetailsView.as_view(),
        name="user_details",
    ),
    path("logout/", LogoutAllView.as_view(), name="user_logout"),

]
