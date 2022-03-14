from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator as MinValue, MaxValueValidator as MaxValue
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "companies"

    def __str__(self):
        return self.name


class Platform(models.Model):
    PLATFORMS = (
        ('android', 'Android'), ('ios', 'iOS'), ('microsoft windows', 'Microsoft Windows'),
        ('ps4', 'PS4'), ('ps5', 'PS5'), ('xbox one', 'Xbox One'),
        ('xbox series X/S', 'Xbox Series X/S'), ('wii u', 'Wii U'),
        ('nintendo 3ds', 'Nintendo 3DS'), ('nintendo switch', 'Nintendo Switch')
    )

    name = models.CharField(max_length=128, choices=PLATFORMS)

    class Meta:
        db_table = "platforms"

    def __str__(self):
        return self.name


class Genre(models.Model):
    GENRES = (
        ('action', 'Action'), ('adventure', 'Adventure'), ('fighting', 'Fighting'),
        ('rpg', 'RPG'), ('racing', 'Racing'), ('shooter', 'Shooter'),
        ('simulation', 'Simulation'), ('sports', 'Sports'), ('other', 'Other')
    )

    name = models.CharField(max_length=128, choices=GENRES)

    class Meta:
        db_table = "genres"

    def __str__(self):
        return self.name


class Series(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        db_table = "series"

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=128)
    picture_url = models.CharField(max_length=128)
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='games')
    developer = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='game_developer')
    publisher = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='game_publisher')
    platforms = models.ManyToManyField(Platform, on_delete=models.PROTECT, related_name='games',
                                       through='GameVersion', null=True, blank=True)
    ratings = models.ManyToManyField(User, on_delete=models.PROTECT, related_name='games', through='Rating')
    threads = models.ManyToManyField(User, on_delete=models.PROTECT, related_name='games', through='Thread')
    series = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='games', null=True, blank=True)
    release_year = models.PositiveIntegerField(validators=[MinValue(1950), MaxValue(date.today().year + 1)])

    class Meta:
        db_table = "titles"

    def __str__(self):
        return self.name


class GameVersion(models.Model):
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='game_versions')
    platform = models.ForeignKey(Platform, on_delete=models.PROTECT, related_name='game_versions')

    class Meta:
        db_table = "game_versions"

    def __str__(self):
        return f'{self.game}, {self.platform}'


class Thread(models.Model):
    starter = models.ForeignKey(User, on_delete=models.PROTECT, related_name='threads')
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='threads')
    title = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)
    comments = models.ManyToManyField(User, on_delete=models.PROTECT, related_name='threads', through='Comment')

    class Meta:
        db_table = "threads"

    def __str__(self):
        return f'{self.starter.username}, {self.game}, {self.created_at}'


class Rating(models.Model):
    RATINGS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ratings')
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='ratings')
    rating = models.PositiveIntegerField(choices=RATINGS)

    class Meta:
        db_table = "ratings"

    def __str__(self):
        return f'{self.user}, {self.game}, {self.rating}'


class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.PROTECT, related_name='comment_thread')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comment_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f'{self.user}, {self.thread.game}, {self.thread.title}'
