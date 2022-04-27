from rest_framework import serializers
from django.contrib.auth.models import User
from gs_django_app.models import Game, Post, Comment, Rating, PostResponse


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'
        depth = 3


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        depth = 3


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        depth = 3


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostResponse
        fields = '__all__'
        depth = 2


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 2


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['username', 'password', 'first_name', 'last_name']
#
#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         instance = super().create(validated_data)
#         instance.user.set_password(password)
#
#         instance.user.save()
#         return instance
