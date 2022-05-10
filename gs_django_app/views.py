from django.db.models import Avg
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from gs_django_app.models import Game, Rating, Post, PostResponse
from gs_django_app.serializers import GameSerializer, RatingSerializer, PostSerializer, ResponseSerializer


@api_view(['POST'])
def signup(request):
    User.objects.create_user(
        username=request.data['username'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name'],
        email=request.data['email'],
        password=request.data['password'])
    return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def current_user(request):
    if request.method == 'GET':
        data = {
            'username': request.user.username,
            'userId': request.user.id
        }
        return Response(data)

    if request.method == 'PUT':
        user = User.objects.get(pk=request.user.id)
        user['first_name'] = request.data.first_name
        user['last_name'] = request.data.last_name


@api_view(['GET', 'POST'])
def games(request):
    if request.method == 'GET':
        game_objects = Game.objects.filter(is_deleted=False)

        if 'searchValue' in request.GET and request.GET['searchValue']:
            game_objects = game_objects.filter(name__icontains=request.GET['searchValue'])

        if 'sort' in request.GET:
            if 'desc' in request.GET['sort']:
                sort_order = '-'
            else:
                sort_order = ''
            game_objects = game_objects.order_by(sort_order + 'name')

        serializer = GameSerializer(game_objects, many=True)
        return Response(serializer.data)

    # elif not request.user.is_superuser:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    #
    # elif request.method == 'POST':
    #     serializer = GameSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def game_details(request, pk):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        def get_genre():
            return f"{game.genre_1}-{game.genre_2}" if game.genre_2 else game.genre_1

        def get_series():
            return game.series.name if game.series else ""

        game_data = {
            "id": game.id,
            "name": game.name,
            "publisher": game.publisher.name,
            "developer": game.developer.name,
            "series": get_series(),
            "release_year": game.release_year,
            "picture_url": game.picture_url,
            "genre": get_genre(),
        }
        return Response(game_data)

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
        ratings = Rating.objects.filter(game_id=pk, is_deleted=False)

        def get_avg_rating():
            if not ratings:
                return 0
            return ratings.aggregate(Avg('score')).get('score__avg')

        def get_user_rating():
            if not ratings:
                return 0, 0
            user_ratings = ratings.filter(user_id=request.user.id)
            if not user_ratings:
                return 0, 0
            if len(user_ratings) == 1:
                return ratings.get(user_id=request.user.id).score, ratings.get(user_id=request.user.id).id
            return user_ratings.latest('updated_at').score, user_ratings.latest('updated_at').id

        rating_data = {
            'avg_rating': get_avg_rating(),
            'user_rating_score': get_user_rating()[0],
            'user_rating_id': get_user_rating()[1]
        }
        return Response(rating_data)

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

    elif (not request.user.is_superuser) and (request.user != rating.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        rating.score = request.data['rating']
        rating.game_id = request.data['game']
        rating.user_id = request.user.id
        rating.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
            responses = PostResponse.objects.filter(post_id=post.id)

            def get_user_response():
                try:
                    user_post_response = responses.get(user_id=request.user.id)
                except PostResponse.DoesNotExist:
                    return ''
                return user_post_response.response

            post_list.append(
                {
                    'post_id': post.id,
                    'username': post.user.username,
                    'user_response': get_user_response(),
                    'likes': responses.filter(response='like').count(),
                    'dislikes': responses.filter(response='dislike').count(),
                    'text': post.text
                }
            )
        return Response(post_list, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        Post.objects.create(
            user_id=request.user.id,
            game_id=request.data['game'],
            text=request.data['text'])
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
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

    elif (not request.user.is_superuser) and (request.user != post.user):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        post.is_deleted = True
        post.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def post_responses(request):
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    user_responses = PostResponse.objects.filter(
        is_deleted=False, post_id=request.data['post'], user_id=request.user.id)

    if len(user_responses):
        user_response = user_responses[0].response
        user_responses.delete()
        if user_response == request.data['response']:
            return Response(status=status.HTTP_204_NO_CONTENT)

    PostResponse.objects.create(
        user_id=request.user.id,
        response=request.data['response'],
        post_id=request.data['post']
    )
    return Response(status=status.HTTP_201_CREATED)


# @api_view(['GET', 'POST'])
# def post_comments(request, pk):
#     if request.method == 'GET':
#         comments = Comment.objects.filter(is_deleted=False, post_id=pk)
#         comment_list = []
#         for comment in comments:
#             comment_list.append(
#                 {
#                     'comment_id': comment.id,
#                     'username': comment.user.username,
#                     'text': comment.text
#                 }
#             )
#         return Response(comment_list, status=status.HTTP_200_OK)
#
#     # # Other method/s will require for the user to be a registered user (or superuser, who is a reg. user)
#
#     elif request.method == 'POST':
#         if not request.user.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#
#         Comment.objects.create(
#             user_id=request.user.id,
#             post_id=request.data['post'],
#             text=request.data['text'])
#         return Response(status=status.HTTP_201_CREATED)


# @api_view(['GET', 'PUT', 'DELETE'])
# def comment_details(request, pk):
#     try:
#         instance = Comment.objects.get(pk=pk)
#     except Comment.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = CommentSerializer(instance)
#         return Response(serializer.data)
#
#     # # Other method/s will require for the user to be the original user or superuser.
#
#     elif (not request.user.is_superuser) and (request.user != instance.user):
#         return Response(status=status.HTTP_401_UNAUTHORIZED)
#
#     elif request.method == 'PUT':
#         serializer = CommentSerializer(instance, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         instance.is_deleted = True
#         return Response(status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET'])
# def jokes(request):
#     response = requests.get('https://v2.jokeapi.dev/joke/Any?safe-mode')
#     jokeData = json.loads(response.content)
#     return Response(jokeData)

