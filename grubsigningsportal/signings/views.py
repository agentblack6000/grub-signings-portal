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
    

class GetQR(APIView):
    """
    Gets QR code for a ticket
    """

    permission_classes = [IsStudent | IsManager | IsDVMUser | IsAdmin]

    def get(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, grub_id):
        try:
            ticket = Ticket.objects.filter(
                user=Student.objects.get(user=request.user), 
                status=Ticket.Status.ACTIVE, grub = grub_id
                ) # tries to get ticket to confirm it exists
        except Ticket.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        generated_hash = generate_hash(request.user.id)
        return Response({"qr_message": generated_hash}, status=status.HTTP_200_OK)


class ScanQR(APIView):
    """
    Scans ticket and updates status
    """

    permission_classes = [(IsManager | IsAdmin)]

    def get(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request, message):
        # TODO: Rewrite to access data from URL
        if verify_hash(message):
            return Response(
                status=status.HTTP_403_FORBIDDEN
            )  # this means data from qr is either tampered or expired
        else:
            user = message.split(":")[0]
            try:
                ticket = Ticket.objects.get(
                    user=str(user), status=Ticket.Status.ACTIVE
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
