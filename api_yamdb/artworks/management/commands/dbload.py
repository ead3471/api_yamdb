import csv, sqlite3
from django.core.management.base import BaseCommand

from artworks.models import Category, Genre, Title#, Comment, Review
from users.models import User

MODELS = {
    'category': Category,
#    'comments': Comment,
    'genre': Genre,
#    'review': Review,
    'titles': Title,
    'users': User,
}

class Command(BaseCommand):

    help = 'Loads data from csv-file into SQLite database'

    def load_model(self, model_name):
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        with open(f'./static/data/{model_name}.csv', 'r') as in_file:
            reader = csv.reader(in_file)
            columns = next(reader)

            for field in reader:
                cur.execute('INSERT INTO users_user VALUES (?,?,?,?,?,?,?);', field)

        

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
#        parser.add_argument(
#            '-q',
#            '--quiet',
#            action='store_true',
#            help='Don\'t ask for action confirmation'
#        )

    def handle(self, *args, **options):
        model_list = []
        if options['model'] == 'all':
            model_list = list(MODELS)
        else:
            model_list.append(options['model'])
        for model in model_list:
#            if not options['quiet']:
#                self.stdout.write(f'You are about to delete all data from {model} model.')
#                confirmation = input('Please confirm [y/n]: ')
#                if confirmation == 'n':
#                    continue
            self.load_model(model)
