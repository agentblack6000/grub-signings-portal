from django.contrib import admin
from .models import Student, Grub, Ticket, Transaction
# Register your models here.

admin.site.register(Student)
admin.site.register(Grub)
admin.site.register(Ticket)
admin.site.register(Transaction)
