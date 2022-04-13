from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator as MinValue, MaxValueValidator as MaxValue
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = "companies"
        ordering = ("name",)

    def __str__(self):
        return self.name


# # Undecided yet about using platforms. If I do, Platform will be a model and have M2M rel. with Game

# class Platform(models.Model):
#     PLATFORMS = (
#         ('android', 'Android'), ('ios', 'iOS'), ('microsoft windows', 'Microsoft Windows'),
#         ('ps4', 'PS4'), ('ps5', 'PS5'), ('xbox one', 'Xbox One'),
#         ('xbox series X/S', 'Xbox Series X/S'), ('wii u', 'Wii U'),
#         ('nintendo 3ds', 'Nintendo 3DS'), ('nintendo switch', 'Nintendo Switch')
#     )
#
#     name = models.CharField(max_length=128, choices=PLATFORMS)
#
#     class Meta:
#         db_table = "platforms"
#
#     def __str__(self):
#         return self.name
#

# # Genre is at this point two fields of Game, may yet change it to a model.

# class Genre(models.Model):
#     GENRES = (
#         ('action', 'Action'), ('adventure', 'Adventure'), ('fighting', 'Fighting'),
#         ('rpg', 'RPG'), ('racing', 'Racing'), ('shooter', 'Shooter'),
#         ('simulation', 'Simulation'), ('sports', 'Sports'), ('other', 'Other')
#     )
#
#     name = models.CharField(max_length=128, choices=GENRES)
#
#     class Meta:
#         db_table = "genres"
#
#     def __str__(self):
#         return self.name

# # Games related to each other will share series, like FIFA games.

class Series(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = "series"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Game(models.Model):
    GENRES = (
        ('Action', 'Action'), ('Adventure', 'Adventure'), ('Fighting', 'Fighting'),
        ('Role playing', 'Role playing'), ('Racing', 'Racing'), ('Shooter', 'Shooter'),
        ('Simulation', 'Simulation'), ('Sports', 'Sports'), ('Stealth', 'Stealth'),
        ('Other', 'Other')
    )

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, default="")
    developer = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='games_developed')
    publisher = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='games_published')
    series = models.ForeignKey(Series, on_delete=models.PROTECT, related_name='games', null=True, blank=True)
    release_year = models.PositiveIntegerField(validators=[MinValue(1950), MaxValue(date.today().year + 1)])
    picture_url = models.CharField(max_length=256)
    ratings = models.ManyToManyField(User, related_name='games_rated', through='Rating')
    posts = models.ManyToManyField(User, related_name='games_posted', through='Post')
    is_deleted = models.BooleanField(default=False)
    genre_1 = models.CharField(max_length=128, choices=GENRES)
    genre_2 = models.CharField(max_length=128, choices=GENRES, null=True, blank=True)

    # OR
    # genre = models.ManyToManyField(Genre, through='GameGenre')
    # platforms = models.ManyToManyField(Platform, through='PlatformGame')

    class Meta:
        db_table = "games"
        ordering = ("name", 'publisher')

    def __str__(self):
        return self.name


# # If genre becomes a model, Game and Genre will have M2M through GameGenre

# class GameGenre(models.Model):
#     game = models.ForeignKey(Game, on_delete=models.PROTECT)
#     genre = models.ForeignKey(Genre, on_delete=models.PROTECT)
#
#     class Meta:
#         db_table = "game_versions"
#
#     def __str__(self):
#         return f'{self.game}, {self.platform}'

# # PlatformGame class will be created if and when I decide to use a Platform model and
# # thus create M2M relationship between Game and Platform through this model. Undecided yet.

# class PlatformGame(models.Model):
#     game = models.ForeignKey(Game, on_delete=models.PROTECT)
#     platform = models.ForeignKey(Platform, on_delete=models.PROTECT)
#
#     class Meta:
#         db_table = "platform_games"
#
#     def __str__(self):
#         return f'{self.game}, {self.platform}'


# # Registered users can rate a game, and remove and change that rating. One instance per user.

class Rating(models.Model):
    # RATINGS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10))

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    # score = models.PositiveIntegerField(choices=RATINGS)
    score = models.PositiveIntegerField(validators=[MinValue(1), MaxValue(10)])

    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "ratings"
        ordering = ("game", "score")

    def __str__(self):
        return f'{self.user}, {self.game}, {self.score}'


# # A registered user can start a discussion post, which will have comments created under it

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    text = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comments = models.ManyToManyField(User, related_name='posts', through='Comment')
    is_deleted = models.BooleanField(default=False)
    # is_closed = models.BooleanField(default=False)

    # # Will look into how to implement is_closed, probably through a simple serializer, starter/superuser only
    # # Will prevent posting of comments to this post when True

    class Meta:
        db_table = "posts"

    def __str__(self):
        return f'{self.user.username}, {self.game}, {self.created_at}'


# # The whole approach to how to handle comments needs to be well planned.
# # Comments will be created, retrieved and viewed through the post they belong to.

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    text = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "comments"

    def __str__(self):
        return f'{self.user.username}, {self.post.game}, {self.post.text}'
