from django.urls import path
from .views import *

urlpatterns = [
    path("login/", view=UserLoginView.as_view(), name="user-login"),
    path("create-grub/", view=CreateGrub.as_view(), name="create-grub"),
    path("data-analytics/", view=ViewDataAnalytics.as_view(), name="data-analytics"),
    path("create-ticket/", view=CreateTicket.as_view(), name="create-ticket"),
    path("display-user/", view=DisplayUser.as_view(), name="display-user"),
    path("cancel-ticket/", view=CancelTicket.as_view(), name="cancel-ticket"),
]
