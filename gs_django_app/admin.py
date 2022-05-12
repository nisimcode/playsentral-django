from django.contrib import admin

from .models import *


@admin.register(PostResponse)
class PostResponseAdmin(admin.ModelAdmin):
    list_filter = ['created_at']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = ['created_at']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_filter = ['score']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_filter = ['name']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ['name']


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_filter = ['name']


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_filter = ['created_at']

# @admin.register(CommentResponse)
# class CommentResponseAdmin(admin.ModelAdmin):
#     list_filter = ['created_at']