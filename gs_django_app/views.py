from django.db.models import Avg
from django.shortcuts import render
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User


from gs_django_app.models import Game, Rating, Post, Comment, Company, Series
from gs_django_app.serializers import GameSerializer, RatingSerializer, CommentSerializer, \
    UserSerializer, PostSerializer


# # For all relevant views, I may yet choose to allow superusers to get a list of
# # all instances but other users to get only a list of instances with is_deleted=False


@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    if request.method == 'GET':
        return Response(request.user.username)

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


# @api_view(['GET', 'POST'])
# def game_posts(request, pk):
#     if request.method == 'GET':
#         post_objs = Post.objects.filter(is_deleted=False, game=pk)
#         posts_list = []
#         for post in post_objs:
#             posts_list.append(
#                 {'id': post.id,
#                  'starter': post.starter.username,
#                  'game': post.game.name,
#                  'title': post.title})
#         return Response(posts_list)
#
#     # # Other method/s will require superuser credentials
#
#     elif not request.user.is_superuser:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#
#     elif request.method == 'POST':
#         serializer = GameSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def game_details(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # def get_avg_rating():
        #     return Rating.objects.filter(game=pk).aggregate(Avg('score')).get('score__avg')

        def get_genre():
            return f"{game.genre_1}-{game.genre_2}" if game.genre_2 else game.genre_1

        ret_data = {
            "id": game.id,
            "name": game.name,
            "publisher": game.publisher.name,
            "developer": game.developer.name,
            "series": game.series.name if game.series else "",
            "release_year": game.release_year,
            "picture_url": game.picture_url,
            "genre": get_genre(),
            # "avg_rating": get_avg_rating()
        }
        return Response(ret_data)

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
        game.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def game_ratings(request, pk):
    if request.method == 'GET':
        game_ratings = Rating.objects.filter(game_id=pk)

        def get_avg_rating():
            avg = game_ratings.aggregate(Avg('score')).get('score__avg')
            if avg:
                return game_ratings.aggregate(Avg('score')).get('score__avg')
            else:
                return 0

        def get_user_rating():
            ratings = game_ratings.filter(user_id=request.user.id)
            if len(ratings) == 1:
                return ratings.get(user_id=request.user.id)
            # if len(ratings) > 1:
            #    pass

        avg_rating = get_avg_rating()
        user_rating_score = get_user_rating().score if get_user_rating() else 0
        user_rating_id = get_user_rating().id if get_user_rating() else 0
        ret_data = {
            'avg_rating': avg_rating,
            'user_rating_score': user_rating_score,
            'user_rating_id': user_rating_id
        }
        return Response(ret_data)

    # # Other method/s will require for the user to be a registered user (or superuser, who is a reg. user)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.data['rating'].isdigit():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if int(request.data['rating']) > 10:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        Rating.objects.create(
            user_id=request.user.id,
            game_id=request.data['game'],
            score=request.data['rating'])
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def rating_details(request, pk):
    try:
        rating = Rating.objects.get(pk=pk)
    except Rating.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RatingSerializer(rating)
        return Response(serializer.data)

    # # Other method/s will require for the user to be the original user.

    elif (not request.user.is_superuser) and (request.user != rating.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        rating.score = request.data['rating']
        rating.game_id = request.data['game']
        rating.user_id = request.user.id
        rating.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # serializer = RatingSerializer(rating_obj, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        rating.is_deleted = True
        rating.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def game_posts(request, pk):
    if request.method == 'GET':
        posts = Post.objects.filter(is_deleted=False, game_id=pk)
        post_list = []
        for post in posts:
            post_list.append(
                {'id': post.id,
                 'user': post.user.username,
                 'game': post.game.name,
                 'text': post.text})
        return Response(post_list, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        Post.objects.create(
            user_id=request.user.id,
            game_id=request.data['game'],
            text=request.data['text'])
        return Response(status=status.HTTP_201_CREATED)
    # if request.method == 'GET':
    #     all_objects = Post.objects.filter(is_deleted=False)
    #     serializer = PostSerializer(all_objects, many=True)
    #     return Response(serializer.data)
    #
    # # # Other method/s will require for the user to be a registered user (or superuser, who is a reg. user)
    #
    # elif not request.user.is_authenticated:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    #
    # elif request.method == 'POST':
    #     serializer = PostSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_details(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        print(post.text)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)

    # # Other method/s will require for the user to be the original user or superuser.

    elif (not request.user.is_superuser) and (request.user != post.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        post.text = request.data['text']
        post.game_id = request.data['game']
        post.user_id = request.user.id
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
        # serializer = PostSerializer(post, data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.is_deleted = True
        post.save()
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


