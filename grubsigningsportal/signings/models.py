from django.db import models
from django.contrib.auth.models import AbstractUser

# TODO: review

class CustomUser(AbstractUser):
    dues = models.PositiveIntegerField(default=0) # usually grub prices are a whole number
    def __str__(self):
        return self.username

class Grub(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price_veg = models.PositiveIntegerField(null=True, blank=True)
    price_nonveg = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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
    amount = models.IntegerField()
    # figure out amount in views instead of auto assigning; couldn't think if a simpler implementation for this
    def __str__(self):
        return (f"{self.ticket.user.username} - {self.ticket.grub.name} - {self.amount}")
