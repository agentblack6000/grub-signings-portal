from django.urls import path
from .views import UserLoginView

urlpatterns = [
    path("login/", view=UserLoginView.as_view(), name="user-login"),
]
