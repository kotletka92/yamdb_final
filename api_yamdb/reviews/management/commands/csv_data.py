import csv
import pathlib

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

FILENAMES = []
FILENAMES.append('users')
FILENAMES.append('category')
FILENAMES.append('titles')
FILENAMES.append('genre')
FILENAMES.append('genre_title')
FILENAMES.append('review')
FILENAMES.append('comments')


class Command(BaseCommand):
    help = 'Populate sqlite with data from csv file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **options):

        filename = options['filename']
        if filename == 'all':
            for item in FILENAMES:
                start_uploading_data(self, item)

        else:
            if filename not in FILENAMES:
                self.stdout.write(
                    'Unknown filename in options.',
                    ' Please pass the correct filename ',
                    '[category, comments, genre_title, genre, review,',
                    ' titles, users]')
                return
            start_uploading_data(self, filename)


def start_uploading_data(self, filename):
    review_csv_file = pathlib.Path(settings.BASE_DIR).joinpath(
        'static/data/' + filename + '.csv')
    with open(review_csv_file, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        if filename == 'users':
            upload_users(self, reader, filename)
        if filename == 'titles':
            upload_titles(self, reader, filename)
        if filename == 'category':
            upload_categories(self, reader, filename)
        if filename == 'genre':
            upload_genres(self, reader, filename)
        if filename == 'genre_title':
            upload_genres_titles(self, reader, filename)
        if filename == 'review':
            upload_reviews(self, reader, filename)
        if filename == 'comments':
            upload_comments(self, reader, filename)


def upload_users(self, reader, filename):
    for row in reader:
        User.objects.get_or_create(id=row['id'],
                                   username=row['username'],
                                   email=row['email'],
                                   first_name=row['first_name'],
                                   last_name=row['last_name'])
    self.stdout.write(f'Succesuful uploaded from file {filename}.csv')


def upload_titles(self, reader, filename):
    for row in reader:
        category, status = Category.objects.get_or_create(id=row['category'])
        Title.objects.get_or_create(id=row['id'],
                                    name=row['name'],
                                    year=row['year'],
                                    category=category)
    self.stdout.write(f'Succesuful uploaded from file {filename}.csv')


def upload_reviews(self, reader, filename):
    for row in reader:
        title, status = Title.objects.get_or_create(id=row['title_id'])
        author, status = User.objects.get_or_create(id=row['author'])
        row_id = row['id']
        try:
            Review.objects.get_or_create(id=row_id,
                                         author=author,
                                         text=row['text'],
                                         title=title,
                                         score=row['score'],
                                         pub_date=row['pub_date'])
        except Exception as error:
            self.stdout.write(f'{error} {row_id}')
    self.stdout.write(f'Succesuful uploaded from file {filename}.csv')


def upload_genres(self, reader, filename):
    for row in reader:
        Genre.objects.get_or_create(id=row['id'],
                                    name=row['name'],
                                    slug=row['slug'])
    self.stdout.write(f'Succesuful uploaded from file {filename}.csv')


def upload_genres_titles(self, reader, filename):
    for row in reader:
        genre, status = Genre.objects.get_or_create(id=row['genre_id'])
        title, status = Title.objects.get_or_create(id=row['title_id'])

        GenreTitle.objects.get_or_create(id=row['id'],
                                         title=title,
                                         genre=genre)
    self.stdout.write(f'Succesuful uploaded from file {filename}.csv')


def upload_comments(self, reader, filename):
    for row in reader:
        review, status = Review.objects.get_or_create(id=row['review_id'])
        author, status = User.objects.get_or_create(id=row['author'])
        Comment.objects.get_or_create(id=row['id'],
                                      author=author,
                                      text=row['text'],
                                      review=review,
                                      pub_date=row['pub_date'])
    self.stdout.write(f'Succesuful uploaded from file {filename}.csv')


def upload_categories(self, reader, filename):
    for row in reader:
        Category.objects.get_or_create(id=row['id'],
                                       name=row['name'],
                                       slug=row['slug'])
    self.stdout.write(f'Succesuful uploaded from file {filename}.csv')
