"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from movies import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('movies.urls')),
# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Existing user and movie URLs
    path('', include('movies.urls')),

    # Custom Admin URLs

    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),
    path('admin-add-movie/', views.admin_add_movie, name='admin_add_movie'),

    path('admin-manage-movies/', views.admin_manage_movies, name='admin_manage_movies'),

    path('admin-edit-movie/<int:movie_id>/', views.admin_edit_movie, name='admin_edit_movie'),

    path('admin-delete-movie/<int:movie_id>/', views.admin_delete_movie, name='admin_delete_movie'),

    path('admin-manage-genres/', views.admin_manage_genres, name='admin_manage_genres'),
    path('admin-add-genre/', views.admin_add_genre, name='admin_add_genre'),
    path('admin-edit-genre/<int:genre_id>/', views.admin_edit_genre, name='admin_edit_genre'),
    path('admin-delete-genre/<int:genre_id>/', views.admin_delete_genre, name='admin_delete_genre'),
    path('admin-manage-users/', views.admin_manage_users, name='admin_manage_users'),
    path('admin-toggle-user/<int:user_id>/',views.admin_toggle_user,name='admin_toggle_user'),

    path('admin-manage-reviews/',views.admin_manage_reviews,name='admin_manage_reviews'),
    path('admin-delete-review/<int:review_id>/',views.admin_delete_review,name='admin_delete_review'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )