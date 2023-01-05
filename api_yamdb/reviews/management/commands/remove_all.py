from django.core.management.base import BaseCommand, CommandError
from reviews.models import User, Title


class Command(BaseCommand):

    def handle(self, *args, **options):
        titles = Title.objects.all()
        for title in titles:
            print(title.name)
