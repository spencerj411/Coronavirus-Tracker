from django.core.management.base import BaseCommand
from main.models import Confirmed
from main.models import Deaths

class Command(BaseCommand):
    help = 'Deletes all records in the database'

    def handle(self, *args, **kwargs):
        Confirmed.objects.all().delete()
        Deaths.objects.all().delete()
        self.stdout.write('Databases wiped!!')
