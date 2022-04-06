from django.contrib import admin

from .models import *


admin.site.register(Rating)
admin.site.register(Thread)
admin.site.register(Comment)


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_filter = ['name']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_filter = ['name']


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    list_filter = ['name']



