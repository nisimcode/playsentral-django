from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from gs_django_app.models import Game, Rating, Thread, Comment
from gs_django_app.serializers import GameSerializer, RatingSerializer, ThreadSerializer, CommentSerializer


# # For all relevant views, I may yet choose to allow superusers to get a list of
# # all instances but other users to get only a list of instances with is_deleted=False

@api_view(['GET', 'POST'])
def games(request):
    if request.method == 'GET':
        all_objects = Game.objects.filter(is_deleted=False)
        serializer = GameSerializer(all_objects, many=True)
        print(serializer.data)
        return Response(serializer.data)

    # # Other method/s will require superuser credentials

    # elif not request.user.is_superuser:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def game_details(request, pk):
    try:
        instance = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GameSerializer(instance)
        return Response(serializer.data)

    # # Other method/s will require superuser credentials

    # elif not request.user.is_superuser:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        serializer = GameSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.is_deleted = True
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def ratings(request):
    if request.method == 'GET':
        all_objects = Rating.objects.filter(is_deleted=False)
        serializer = RatingSerializer(all_objects, many=True)
        print(serializer.data)
        return Response(serializer.data)

    # # Other method/s will require for the user to be a registered user (or superuser, who is a reg. user)

    # elif not request.user.is_authenticated:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'POST':
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def rating_details(request, pk):
    try:
        instance = Rating.objects.get(pk=pk)
    except Rating.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RatingSerializer(instance)
        return Response(serializer.data)

    # # Other method/s will require for the user to be the original user or superuser.

    # elif (not request.user.is_superuser) and (request.user != instance.user):
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        serializer = RatingSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.is_deleted = True
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def threads(request):
    if request.method == 'GET':
        all_objects = Thread.objects.filter(is_deleted=False)
        serializer = ThreadSerializer(all_objects, many=True)
        print(serializer.data)
        return Response(serializer.data)

    # # Other method/s will require for the user to be a registered user (or superuser, who is a reg. user)

    # elif not request.user.is_authenticated:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'POST':
        serializer = ThreadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def thread_details(request, pk):
    try:
        instance = Thread.objects.get(pk=pk)
    except Thread.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ThreadSerializer(instance)
        return Response(serializer.data)

    # # Other method/s will require for the user to be the original user or superuser.

    # elif (not request.user.is_superuser) and (request.user != instance.user):
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        serializer = ThreadSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.is_deleted = True
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def comments(request):
    if request.method == 'GET':
        all_objects = Comment.objects.filter(is_deleted=False)
        serializer = CommentSerializer(all_objects, many=True)
        print(serializer.data)
        return Response(serializer.data)

    # # Other method/s will require for the user to be a registered user (or superuser, who is a reg. user)

    # elif not request.user.is_authenticated:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def comment_details(request, pk):
    try:
        instance = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CommentSerializer(instance)
        return Response(serializer.data)

    # # Other method/s will require for the user to be the original user or superuser.

    # elif (not request.user.is_superuser) and (request.user != instance.user):
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        serializer = CommentSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.is_deleted = True
        return Response(status=status.HTTP_204_NO_CONTENT)