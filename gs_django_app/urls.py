from django.urls import path

from . import views

# Creating URLConf
# api/v1/restaurants GET | POST
# api/v1/restaurants/1 GET | PUT | PATCH | DELETE

# api/v1/restaurants/1/reviews GET | POST
# api/v1/restaurants/1/reviews/11 GET | PUT | PATCH | DELETE

# api/v1/userprofile/current

# api/v1/reviews GET | POST


urlpatterns = [
    path("games/", views.games),
    path("games/<int:pk>", views.game_details),
    # path("reviews/", views.reviews),
    path("games/<int:pk>/threads", views.game_threads),
    path("games/<int:pk>/reviewss", views.game_reviews),
    # path("reviews/<int:pk>", views.review_details),
    # path("reviews/<int:pk>", views.user_reviews)
]
