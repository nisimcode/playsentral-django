from rest_framework import serializers
from rest_framework import fields

from gs_django_app.models import Game, Post, Rating, PostResponse, Note


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


# class NoteSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     details = fields.CharField(required=True, max_length=256)
#     text = fields.CharField(required=True, max_length=256)
#
#     def create(self, validated_data):
#         return Note.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.details = validated_data.get('details', instance.details)
#         instance.text = validated_data.get('text', instance.text)
#         instance.save()
#         return instance


# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'
#         depth = 2


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
