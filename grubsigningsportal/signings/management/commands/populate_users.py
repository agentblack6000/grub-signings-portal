from django.core.management.base import BaseCommand

class Command(BaseCommand):
    # TODO: Create some base users and load them based on the model implemented for students
    # TODO: use user.objects.create_user() instead of just create() so password is hashed automatically
    
    def handle(self, *args, **options):
        pass
    