from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token


from . import views

# Initial URLS, subject to many changes. For example, most likely no use for
# comments link, they will be accessed only through the thread they belong to.

urlpatterns = [
    path('token/', obtain_auth_token),
    path('signup/', views.signup),
    path("users/current", views.current_user),
    path("games/", views.games),
    path("games/<int:pk>/details", views.game_details),
    path("games/<int:pk>/posts", views.game_posts),
    path("games/<int:pk>/ratings", views.game_ratings),
    # path("posts/", views.posts),
    path("posts/<int:pk>", views.post_details),
    # path("ratings/", views.ratings),
    path("ratings/<int:pk>", views.rating_details),
    # path("posts/", views.posts),
    # path("threads/<int:pk>", views.thread_details),
    # path("comments/", views.comments),
    # path("comments/<int:pk>", views.comment_details),


]
