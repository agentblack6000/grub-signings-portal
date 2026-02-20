"""
Populate some users in the database
"""
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from signings.models import Student

from decimal import Decimal
import csv


class Command(BaseCommand):
    help = "Populate some users in the database"
    
    def handle(self, *args, **options):
        with open("userdata.csv", "r") as user_data_file:
            reader = csv.DictReader(user_data_file)
            student_group = Group.objects.get(name="student")

            for row in reader:
                user = User.objects.create_user(
                    username=row["username"],
                    password=row["password"],
                    email=row["email"],
                )

                student = Student.objects.create(
                    user=user,
                    dues=Decimal("0.00"),
                )

                student.user.groups.add(student_group)
                student.save()
