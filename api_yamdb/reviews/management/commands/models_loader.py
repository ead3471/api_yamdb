from ._private import ModelLoader, TitleLoader, ModelWithFKLoader
from django.core.management.base import BaseCommand, CommandParser
from reviews.models import Category, Genre, Title, Review, Comment
import pathlib
from django.contrib.auth import get_user_model
from typing import Dict
User = get_user_model()


class Command(BaseCommand):

    base_data_file_location = (pathlib.Path().absolute() / 'api_yamdb'
                               / "static"
                               / "data")

    loaders_dict: Dict[str, ModelLoader] = {
        "category": ModelLoader(Category,
                                base_data_file_location / "category.csv",
                                "Load Categories"),
        "user": ModelLoader(User,
                            base_data_file_location / "users.csv",
                            "Load Users"),
        "genre": ModelLoader(Genre,
                             base_data_file_location / "genre.csv",
                             "Load Genres"),
        "comment": ModelWithFKLoader(Comment,
                                     base_data_file_location / "comments.csv",
                                     {"review": Review, 'author': User},
                                     "Load Comments"),
        "title": TitleLoader(base_data_file_location / "titles.csv",
                             base_data_file_location / "genre_title.csv",
                             "Load Titles"),
        "review": ModelWithFKLoader(Review,
                                    base_data_file_location / "review.csv",
                                    {"title": Title, 'author': User},
                                    "Load Reviews"),
    }

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('--load',
                            action='store_true',
                            help='Load all data from file')
        parser.add_argument('--show',
                            action='store_true',
                            help='Show all categories')
        parser.add_argument('--delete',
                            action='store_true',
                            help='Delete all categories')
        parser.add_argument('--reload',
                            action='store_true',
                            help='Reload all categories')

        for command, loader in self.loaders_dict.items():
            parser.add_argument(f'--{command}',
                                action='store_true',
                                help=loader)

    def handle(self, *args, **options):
        model_loader = None
        for command in self.loaders_dict.keys():
            if options[command]:
                model_loader = self.loaders_dict[command]
                break
        if not model_loader:
            print(
                ('Loader not found, you should use one'
                 f'of {self.loaders_dict.keys()} values'))
            return

        if options['load']:
            model_loader.load()
            return

        if options['show']:
            model_loader.show()
            return

        if options['delete']:
            model_loader.remove()
            return

        if options['reload']:
            model_loader.reload()
            return

        print("Action is not set")