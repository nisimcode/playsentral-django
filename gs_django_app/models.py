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

    class Meta:
        db_table = "games"
        ordering = ("name", 'publisher')

    def __str__(self):
        return self.name

# # Registered users can rate a game, and remove and change that rating. One instance per user.


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
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
    is_deleted = models.BooleanField(default=False)
    responses = models.ManyToManyField(User, related_name='posts_liked', through='PostResponse')
    comments = models.ManyToManyField(User, related_name='posts_commented', through='Comment')

    # is_closed = models.BooleanField(default=False)

    # # Will look into how to implement is_closed, probably through a simple serializer, starter/superuser only
    # # Will prevent posting of comments to this post when True

    class Meta:
        db_table = "posts"
        ordering = ("created_at",)

    def __str__(self):
        return f'{self.user.username}, {self.game}, {self.created_at}'


class PostResponse(models.Model):
    RESPONSES = (('like', 'like'), ('dislike', 'dislike'))

    response = models.CharField(choices=RESPONSES, max_length=16)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "post_responses"
        ordering = ('response', 'user', 'created_at')

    def __str__(self):
        return self.response


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
