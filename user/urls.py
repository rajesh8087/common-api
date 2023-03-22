from django.urls import path
from .views import *

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("change-password/", UserChangePasswordView.as_view(), name="changepassword"),
    path(
        "send-reset-password-email/",
        SendPasswordResetEmailView.as_view(),
        name="send-reset-password-email",
    ),
    path(
        "reset-password/<uid>/<token>/",
        UserPasswordResetView.as_view(),
        name="reset-password",
    ),
    path("list-users/", ListUsersView.as_view(), name="all-users"),
    path("get-user/<int:pk>/", UserView.as_view(), name="user-detail"),
    path("delete-user/<int:pk>/", UserView.as_view(), name="delete-user"),
    path("update-user/<int:pk>/", UserView.as_view(), name="update-user"),
    path(
        "get-child/employees/",
        FetchChildEmployeeView.as_view(),
        name="get-child-employees",
    ),
]
