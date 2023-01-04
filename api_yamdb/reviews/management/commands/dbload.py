import csv
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

MODELS = {
    'category': (Category, 'category.csv'),
    'comment': (Comment, 'comments.csv'),
    'genre': (Genre, 'genre.csv'),
    'review': (Review, 'reviews.csv'),
    'title': (Title, 'titles.csv'),
    'user': (User, 'users.csv')
}

class Command(BaseCommand):

    help = 'Loads data from csv-file into SQLite database'

    def load_model(self, model_name):
        rows_list = []
        with open(f'./static/data/{MODELS[model_name][1]}', 'r') as in_file:
            reader = csv.DictReader(in_file)
            for row in reader:
                rows_list.append(MODELS[model_name][0](**row))
        MODELS[model_name][0].objects.bulk_create(rows_list)


    def add_arguments(self, parser):
        parser.add_argument(
            '-m',
            dest='model',
            default='all',
            help=(
                'Model name to load data. Set \'all\' '
                'to execute action for all models. Default - \'all\'.'
            )
        )

    def handle(self, *args, **options):
        model_list = []
        if options['model'] == 'all':
            model_list = list(MODELS)
        else:
            model_list.append(options['model'])
        for model in model_list:
            self.load_model(model.lower())
