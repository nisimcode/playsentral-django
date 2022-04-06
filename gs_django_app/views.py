from django.db.models import Avg
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User


from gs_django_app.models import Game, Rating, Thread, Comment, Company, Series
from gs_django_app.serializers import GameSerializer, RatingSerializer, ThreadSerializer, CommentSerializer, \
    UserSerializer


# # For all relevant views, I may yet choose to allow superusers to get a list of
# # all instances but other users to get only a list of instances with is_deleted=False


@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    if request.method == 'GET':
        data = {
            "first_name": request.user.first_name,
            "last_name": request.user.last_name
        }
        return Response(data)

    if request.method == 'PUT':
        user = User.objects.get(pk=request.user.id)
        user['first_name'] = request.data.first_name
        user['last_name'] = request.data.last_name


@api_view(['GET', 'POST'])
def games(request):
    if request.method == 'GET':
        all_objects = Game.objects.filter(is_deleted=False)
        serializer = GameSerializer(all_objects, many=True)
        return Response(serializer.data)

    # # Other method/s will require superuser credentials

    elif not request.user.is_superuser:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def game_threads(request, pk):
    if request.method == 'GET':
        thread_objs = Thread.objects.filter(is_deleted=False, game=pk)
        threads_list = []
        for thread in thread_objs:
            threads_list.append(
                {'id': thread.id,
                 'starter': thread.starter.username,
                 'game': thread.game.name,
                 'title': thread.title})
        return Response(threads_list)

    # # Other method/s will require superuser credentials

    elif not request.user.is_superuser:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'POST':
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def game_details(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        def get_avg_rating():
            return Rating.objects.filter(game=pk).aggregate(Avg('rating')).get('rating__avg')

        def get_genre():
            return f"{game.genre_1}-{game.genre_2}" if game.genre_2 else game.genre_1

        game_data = {
            "id": game.id,
            "name": game.name,
            "publisher": game.publisher.name,
            "developer": game.developer.name,
            "series": game.series.name if game.series else "",
            "release_year": game.release_year,
            "picture_url": game.picture_url,
            "genre": get_genre(),
            "avg_rating": get_avg_rating()
        }
        return Response(game_data)

    # # Other method/s will require superuser credentials

    elif not request.user.is_superuser:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        serializer = GameSerializer(game, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        game.is_deleted = True
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def ratings(request):
    if request.method == 'GET':
        all_objects = Rating.objects.filter(is_deleted=False)
        serializer = RatingSerializer(all_objects, many=True)
        print(serializer.data)
        return Response(serializer.data)

    # # Other method/s will require for the user to be a registered user (or superuser, who is a reg. user)

    elif not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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

    # # Other method/s will require for the user to be the original user.

    elif (not request.user.is_superuser) and (request.user != instance.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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
        threads = Thread.objects.filter(is_deleted=False)
        thread_list = []
        for thread in threads:
            thread_list.append(
                {'id': thread.id,
                 'starter': thread.starter.username,
                 'game': thread.game.name,
                 'title': thread.title})
        return Response(thread_list)
    elif request.method == 'POST':
        # Thread.objects.create(
        #     # country=request.data['country'],
        #     # city=request.data['city'],
        #     # user=request.user)
        return Response(status=status.HTTP_201_CREATED)
    # if request.method == 'GET':
    #     all_objects = Thread.objects.filter(is_deleted=False)
    #     serializer = ThreadSerializer(all_objects, many=True)
    #     return Response(serializer.data)
    #
    # # # Other method/s will require for the user to be a registered user (or superuser, who is a reg. user)
    #
    # elif not request.user.is_authenticated:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    #
    # elif request.method == 'POST':
    #     serializer = ThreadSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    elif (not request.user.is_superuser) and (request.user != instance.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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

    elif not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

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

    elif (not request.user.is_superuser) and (request.user != instance.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        serializer = CommentSerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        instance.is_deleted = True
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def signup(request):
    User.objects.create_user(
        username=request.data['username'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email'],
        password=request.data['password'])
    return Response(status=status.HTTP_201_CREATED)


