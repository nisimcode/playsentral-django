from datetime import date
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator as MinValue, MaxValueValidator as MaxValue
from django.db import models
from gs_django_app.etc import GAME_GENRES


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Company(BaseModel):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = "companies"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Series(BaseModel):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = "series"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Game(BaseModel):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    developer = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='games_developed')
    publisher = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='games_published')
    series = models.ForeignKey(Series, on_delete=models.PROTECT, related_name='games', null=True, blank=True)
    release_year = models.PositiveIntegerField(validators=[MinValue(1950), MaxValue(date.today().year + 1)])
    picture_url = models.CharField(max_length=256)
    ratings = models.ManyToManyField(User, related_name='games_rated', through='Rating')
    posts = models.ManyToManyField(User, related_name='games_posted', through='Post')
    genre_1 = models.CharField(max_length=128, choices=GAME_GENRES)
    genre_2 = models.CharField(max_length=128, choices=GAME_GENRES, null=True, blank=True)

    class Meta:
        db_table = "games"
        ordering = ("name", "release_year")

    def __str__(self):
        return self.name


class Rating(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    score = models.PositiveIntegerField(validators=[MinValue(1), MaxValue(10)])

    class Meta:
        db_table = "ratings"
        ordering = ("game", "score")

    def __str__(self):
        return self.score


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    game = models.ForeignKey(Game, on_delete=models.PROTECT)
    text = models.CharField(max_length=256)
    responses = models.ManyToManyField(User, related_name='posts_responded', through='PostResponse')
    comments = models.ManyToManyField(User, related_name='posts_commented', through='Comment')

    class Meta:
        db_table = "posts"
        ordering = ("created_at", "text")

    def __str__(self):
        return self.text


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    text = models.CharField(max_length=256)
    responses = models.ManyToManyField(User, related_name='comments_responded', through='CommentResponse')

    class Meta:
        db_table = "comments"
        ordering = ("created_at", "text")

    def __str__(self):
        return self.text


class PostResponse(BaseModel):
    response = models.CharField(choices=(('like', 'like'), ('dislike', 'dislike')), max_length=16)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = "post_responses"
        ordering = ("created_at", "response")

    def __str__(self):
        return self.response


class CommentResponse(BaseModel):
    response = models.CharField(choices=(('like', 'like'), ('dislike', 'dislike')), max_length=16)
    comment = models.ForeignKey(Comment, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = "comment_responses"
        ordering = ("created_at", "response")

    def __str__(self):
        return self.response
