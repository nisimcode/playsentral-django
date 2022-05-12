from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('token/', obtain_auth_token),
    path('signup/', views.signup),
    path("users/current", views.current_user),
    path("games/", views.games),
    path("games/<int:pk>/details", views.game_details),
    path("games/<int:pk>/posts", views.game_posts),
    path("games/<int:pk>/ratings", views.game_ratings),
    path("responses/", views.post_responses),
    path("posts/<int:pk>", views.post_details),
    path("ratings/<int:pk>", views.rating_details),
    path("notes/", views.notes)



]
