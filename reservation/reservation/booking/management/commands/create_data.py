from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def handle(self, *args, **options):
        from booking.utils import *
        create_user()
        create_rooms()
        print "done"
