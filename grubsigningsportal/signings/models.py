from django.contrib.auth.models import AbstractUser
from django.db import models

from decimal import Decimal


# TODO: Review changes

class Student(AbstractUser):
    dues = models.DecimalField(default=0, max_digits=8, decimal_places=2, min_value=Decimal("0.00"))
    def __str__(self):
        return self.username

class Grub(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price_veg = models.DecimalField(null=True, default=0, max_digits=8, decimal_places=2)
    price_nonveg = models.DecimalField(null=True, default=0, max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="tickets")
    grub = models.ForeignKey(Grub, on_delete=models.CASCADE)

    class Type(models.TextChoices):
        VEG = 'VEG', 'Vegetarian'
        NONVEG = 'NONVEG', 'Non-Vegetarian'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        CANCELLED = 'CANCELLED', 'Cancelled'
        USED = 'USED', 'Used'

    type = models.CharField(max_length=10, choices=Type.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return (f"{self.user.username} - {self.grub.name}")

class Transaction(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    class Type(models.TextChoices):
        PAYMENT = 'PAYMENT', 'Payment'
        REFUND = 'REFUND', 'Refund'

    type = models.CharField(max_length=10, choices=Type.choices, default=Type.PAYMENT)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return (f"{self.ticket.user.username} - {self.ticket.grub.name} - {self.amount}")
