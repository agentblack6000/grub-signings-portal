"""
views.py
"""
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserLoginTokenObtainPairSerializer


class UserLoginView(TokenObtainPairView):
    """
    Docstring for UserLoginView
    """
    serializer_class = UserLoginTokenObtainPairSerializer
