# Generated by Django 4.0.3 on 2022-03-15 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gs_django_app', '0010_alter_comment_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='is_closed',
            field=models.BooleanField(default=False),
        ),
    ]