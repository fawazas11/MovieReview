from django.urls import path
from django.contrib.auth import views as auth_views
from .import views


urlpatterns = [
    path('', views.index, name='index'),
    path('movie/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search_movies, name='search_movies'),
    path('genres/', views.genres, name='genres'),
    path('genre/<int:genre_id>/', views.genre_movies, name='genre_movies'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('watchlist/', views.watchlist, name='watchlist'),


    path('dashboard/', views.user_dashboard, name='user_dashboard'),

    path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='forgotpass.html'
        ),
        name='password_reset'
    ),

    path(
        'forgot-password/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),

    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),

    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),

    path('my-reviews/', views.my_reviews, name='my_reviews'),

path(
    "movie/<int:movie_id>/review/",
    views.add_review,
    name="add_review",
),
path("user/movies/", views.user_movies, name="user_movies"),
path("user/genres/", views.user_genres, name="user_genres"),
path("user/watchlist/", views.user_watchlist, name="user_watchlist"),

path(
    "movie/<int:movie_id>/add-watchlist/",
    views.add_to_watchlist,
    name="add_to_watchlist",
),

path(
    "movie/<int:movie_id>/remove-watchlist/",
    views.remove_from_watchlist,
    name="remove_from_watchlist",
),


path(
    'delete-my-review/<int:review_id>/',
    views.delete_my_review,
    name='delete_my_review'
),
path('profile/', views.profile_view, name='profile'),
]