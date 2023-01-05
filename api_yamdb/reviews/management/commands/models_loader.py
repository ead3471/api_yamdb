from django.core.management.base import BaseCommand, CommandError, CommandParser
from reviews.models import Category, Genre, Title, Review, Comment
import csv
import pathlib
from django.db.models.base import ModelBase
from django.db.models import Model
from django.contrib.auth import get_user_model
from typing import Dict
User = get_user_model()


class ModelLoader:
    def __init__(self, model_class: ModelBase, file_location: str, help: str) -> None:
        self.model_class = model_class
        self.file_location = file_location
        self.help = help

    def load(self):
        with open(self.file_location, 'r') as data_file:
            csvreader = csv.DictReader(data_file, delimiter=',')
            objects_list = []
            for row in csvreader:
                objects_list.append(**row)

            self.model_class.objects.bulk_create(objects_list)

    def remove(self):
        self.model_class.objects.all().delete()

    def show(self):
        for object in self.model_class.objects.all():
            print(f'{object.pk}:{object}')

    def reload(self):
        self.remove()
        self.load()


class TitlesLoader(ModelLoader):
    def __init__(self, titles_file: str, genre_titles_file: str, help: str) -> None:
        self.model_class = Title
        self.titles_file = titles_file
        self.genre_titles_file = genre_titles_file
        self.help = help

    def load(self):
        with open(self.titles_file, 'r') as data_file:
            csvreader = csv.DictReader(data_file, delimiter=',')
            for row in csvreader:
                if 'category' in row:
                    category = Category.objects.get(id=row['category'])
                self.model_class.objects.update_or_create(
                    name=row['name'],
                    category=category,
                    year=row['year']
                )

        # with open(self.genre_titles_file, 'r') as genres_file:
        #     csvreader = csv.DictReader(genres_file, delimiter=',')
        #     for row in csvreader:
        #         title_id = row['title_id']
        #         genre_id = row['genre_id']
        #         print(f'{genre_id}->{title_id}')
        #         Title.objects.get(id=title_id).genre.add(
        #             row['genre_id'])


class Command(BaseCommand):

    base_data_file_location = (pathlib.Path().absolute() / 'api_yamdb'
                               / "static"
                               / "data")

    loaders_dict: Dict[str, ModelLoader] = {
        "category": ModelLoader(Category, base_data_file_location / "category.csv", "Load Categories"),
        "user": ModelLoader(User, base_data_file_location / "users.csv", "Load Users"),
        "genre": ModelLoader(Genre, base_data_file_location / "genre.csv", "Load Genres"),
        "comment": ModelLoader(Comment, base_data_file_location / "comments.csv", "Load Comments"),
        "title": TitlesLoader(base_data_file_location / "titles.csv", base_data_file_location / "genre_title.csv", "Load Titles"),
        "review": ModelLoader(Review, base_data_file_location / "review.csv", "Load Reviews"),
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
                f'Loader not found, you should use one of {self.loaders_dict.keys()} values')
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
