from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()

MODELS = {
    'category': Category,
    'comment': Comment,
    'genre': Genre,
    'review': Review,
    'title': Title,
    'user': User
}

class Command(BaseCommand):

    help = 'Loads data from csv-file into SQLite database'

    def clear_model(self, model_name):
        MODELS[model_name].objects.all().delete()

    def add_arguments(self, parser):
        parser.add_argument(
            '-m',
            dest='model',
            default='all',
            help=(
                'Model name to clear data. Set \'all\' '
                'to execute action for all models. Default - \'all\'.'
            )
        )
        parser.add_argument(
            '-q',
            '--quiet',
            action='store_true',
            help='Don\'t ask for action confirmation'
        )

    def handle(self, *args, **options):
        model_list = []
        if options['model'] == 'all':
            model_list = list(MODELS)
        else:
            model_list.append(options['model'])
        for model in model_list:
            if not options['quiet']:
                self.stdout.write(f'You are about to delete all data from {model} model.')
                confirmation = input('Please confirm [y/n]: ')
                if confirmation == 'n':
                    continue
            self.clear_model(model.lower())
