"""
views.py
"""
from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (
    Grub,
    Student,
    Transaction,
    Ticket,
)
from .permissions import IsStudent, IsManager, IsDVMUser, IsAdmin
from .serializers import (
    UserLoginTokenObtainPairSerializer,
)

from .helper import generate_hash, verify_hash

# TODO: Add business logic for views, add/remove views if needed

# Based on the permission classes, the admin must assign user groups from the admin panel
# (Assign manager, dvm) groups; student would be the default managed by the command script)


class UserLoginView(TokenObtainPairView):
    """
    Handles user login through JWT
    """

    permission_classes = (
        []
    )  # Must be overidden since all views require authenticated users
    serializer_class = UserLoginTokenObtainPairSerializer


class CreateGrub(APIView):
    """
    Sets up grub metadata
    """

    permission_classes = [(IsDVMUser | IsAdmin)]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class ViewDataAnalytics(APIView):
    """
    Displays Transactions / Tickets
    Depending on the get request params can show different statistics
    """

    permission_classes = [(IsManager | IsDVMUser | IsAdmin)]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class CreateTicket(APIView):
    """
    Creates a Ticket, Transaction based on data passed
    """

    permission_classes = [(IsManager | IsDVMUser | IsAdmin)]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class DisplayUser(APIView):
    """
    Displays the QR code needed to create a ticket
    """

    permission_classes = [IsStudent]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class CancelTicket(APIView):
    """
    Cancels ticket
    """

    permission_classes = [(IsManager | IsDVMUser | IsAdmin)]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        return Response(status=status.HTTP_200_OK)


class ScanTicket(APIView):
    """
    Scans ticket and updates status
    """

    permission_classes = [(IsManager | IsAdmin)]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, data, request):
        if not verify_hash(data):
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )  # this means data from qr is either tampered or expired
        else:
            user = data.split(":")[0]
            try:
                ticket = Ticket.objects.get(
                    user=user, status=Ticket.Status.ACTIVE, grub=request.grub
                )  # assume grub is known and attached by manager in the request
            except Ticket.DoesNotExist:
                return Response(
                    status=status.HTTP_404_NOT_FOUND
                )  # user doesn't have a valid ticket
            else:
                ticket.status = Ticket.Status.USED
                ticket.save()
                return Response(
                    status=status.HTTP_200_OK
                )  # all ok ticket scanned and marked
