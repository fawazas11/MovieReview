
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, MovieForm,GenreForm

from django.shortcuts import render, redirect
# from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required

# Create your views here.

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg, Q
from .models import Movie, Genre,Watchlist,Review

from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model

# Home page
def index(request):
    movies = Movie.objects.annotate(
        average_rating=Avg('reviews__rating')
    ).order_by('-created_at')

    return render(request, 'home.html', {
        'movies': movies
    })


# # Movie details and reviews
# def movie_detail(request, movie_id):
#     movie = get_object_or_404(
#         Movie.objects.annotate(
#             average_rating=Avg('reviews__rating')
#         ),
#         id=movie_id
#     )
#
#     reviews = movie.reviews.select_related('user').all()
#
#     return render(request, 'movie_detail.html', {
#         'movie': movie,
#         'reviews': reviews
#     })

def movie_detail(request, movie_id):
    movie = get_object_or_404(
        Movie.objects.annotate(
            average_rating=Avg('reviews__rating')
        ),
        id=movie_id
    )

    reviews = movie.reviews.select_related('user').all()

    # Check whether the logged-in user saved this movie
    is_in_watchlist = False

    if request.user.is_authenticated:
        is_in_watchlist = Watchlist.objects.filter(
            user=request.user,
            movie=movie
        ).exists()

    return render(request, 'movie_detail.html', {
        'movie': movie,
        'reviews': reviews,
        'is_in_watchlist': is_in_watchlist,
    })


# Search movies by title, director or description
def search_movies(request):
    query = request.GET.get('q', '').strip()

    movies = Movie.objects.none()

    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(director__icontains=query) |
            Q(description__icontains=query)
        ).annotate(
            average_rating=Avg('reviews__rating')
        )

    return render(request, 'search.html', {
        'movies': movies,
        'query': query
    })


# Display all genres
def genres(request):
    all_genres = Genre.objects.all().order_by('name')

    return render(request, 'genres.html', {
        'genres': all_genres
    })


# Display movies from a selected genre
def genre_movies(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)

    movies = Movie.objects.filter(
        genre=genre
    ).annotate(
        average_rating=Avg('reviews__rating')
    )

    return render(request, 'genre_movies.html', {
        'genre': genre,
        'movies': movies
    })


@login_required
def watchlist(request):
    items = Watchlist.objects.filter(
        user=request.user
    ).select_related('movie')

    return render(request, 'watchlist.html', {
        'watchlist': items
    })



def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('index')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})




def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            messages.success(request, "Successfully logged in!")

            # Check whether the user is an admin
            if user.is_staff:
                return redirect('admin_dashboard')

            # Normal user
            return redirect('user_dashboard')

        else:
            messages.error(request, "Invalid username or password.")

    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Successfully logged out!")

    return redirect('index')



@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have logged out successfully.')
        return redirect('index')

    return redirect('index')


@login_required
def user_dashboard(request):
    reviews = Review.objects.filter(
        user=request.user
    ).select_related('movie')

    watchlist = Watchlist.objects.filter(
        user=request.user
    ).select_related('movie')

    context = {
        'reviews': reviews,
        'watchlist': watchlist,
    }

    return render(request, 'user_dashboard.html', context)






@login_required
def my_reviews(request):
    reviews = (
        Review.objects
        .filter(user=request.user)
        .select_related('movie')
        .order_by('-created_at')
    )

    return render(
        request,
        'my_reviews.html',
        {'reviews': reviews}
    )



@login_required
@require_http_methods(["GET", "POST"])
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    error = None

    if request.method == "POST":
        rating_value = request.POST.get("rating", "").strip()
        comment = request.POST.get("comment", "").strip()

        try:
            rating = int(rating_value)
        except (ValueError, TypeError):
            rating = 0

        if rating < 1 or rating > 5:
            error = "Please select a rating from 1 to 5."
        elif not comment:
            error = "Please write your review."
        else:
            Review.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={
                    "rating": rating,
                    "comment": comment,
                },
            )
            return redirect("movie_detail", movie_id=movie.id)

    return render(request, "add_review.html", {
        "movie": movie,
        "error": error,
    })






# User --> movie,review,watch list,genre

@login_required
def user_movies(request):
    movies = Movie.objects.select_related("genre").all().order_by("title")

    search_query = request.GET.get("q", "").strip()
    genre_id = request.GET.get("genre", "").strip()

    if search_query:
        movies = movies.filter(
            Q(title__icontains=search_query)
            | Q(director__icontains=search_query)
        )

    if genre_id.isdigit():
        movies = movies.filter(genre_id=int(genre_id))

    genres = Genre.objects.all().order_by("name")

    return render(
        request,
        "user_movies.html",
        {
            "movies": movies,
            "genres": genres,
            "search_query": search_query,
            "selected_genre": genre_id,
        },
    )


@login_required
def user_genres(request):
    genres = Genre.objects.all().order_by("name")

    return render(
        request,
        "user_genres.html",
        {"genres": genres},
    )


@login_required
def user_watchlist(request):
    watchlist = (
        Watchlist.objects
        .filter(user=request.user)
        .select_related("movie", "movie__genre")
        .order_by("-added_at")
    )

    return render(
        request,
        "user_watchlist.html",
        {"watchlist": watchlist},
    )


@login_required
@require_POST
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    Watchlist.objects.get_or_create(
        user=request.user,
        movie=movie
    )

    return redirect("movie_detail", movie_id=movie.id)


@login_required
@require_POST
def remove_from_watchlist(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    Watchlist.objects.filter(
        user=request.user,
        movie=movie
    ).delete()

    return redirect("user_watchlist")



# ==============================
# ADMIN LOGIN
# ==============================

def admin_login_view(request):

    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')

        messages.error(
            request,
            'Invalid admin username or password.'
        )

    return render(request, 'admin_panel/add_movie.html')


# ==============================
# ADMIN DASHBOARD
# ==============================

@user_passes_test(
    lambda user: user.is_authenticated and user.is_staff,
    login_url='admin_login'
)
def admin_dashboard(request):

    User = get_user_model()

    context = {
        'total_movies': Movie.objects.count(),
        'total_genres': Genre.objects.count(),
        'total_users': User.objects.count(),
        'total_reviews': Review.objects.count(),
    }

    return render(
        request,
        'admin_panel/admin_dashboard.html',
        context
    )


# ==============================
# ADMIN LOGOUT
# ==============================

@login_required
@require_POST
def admin_logout_view(request):

    if not request.user.is_staff:
        return redirect('index')

    logout(request)

    messages.success(request, 'Admin logged out successfully.')

    return redirect('login')


# ==============================
# ADD MOVIE
# ==============================

@user_passes_test(
    lambda user: user.is_authenticated and user.is_staff
)
def admin_add_movie(request):

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Movie added successfully!')
            return redirect('admin_manage_movies')

    else:
        form = MovieForm()

    return render(request, 'admin_panel/add_movie.html', {
        'form': form
    })


# ==============================
# MANAGE MOVIES
# ==============================

@user_passes_test(
    lambda user: user.is_authenticated and user.is_staff
)
def admin_manage_movies(request):

    movies = Movie.objects.select_related('genre').all().order_by('-created_at')

    return render(request, 'admin_panel/manage_movies.html', {
        'movies': movies
    })


# ==============================
# EDIT MOVIE
# ==============================

@user_passes_test(
    lambda user: user.is_authenticated and user.is_staff
)
def admin_edit_movie(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        form = MovieForm(
            request.POST,
            request.FILES,
            instance=movie
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Movie updated successfully!')
            return redirect('admin_manage_movies')

    else:
        form = MovieForm(instance=movie)

    return render(request, 'admin_panel/edit_movie.html', {
        'form': form,
        'movie': movie
    })


# ==============================
# DELETE MOVIE
# ==============================

@user_passes_test(
    lambda user: user.is_authenticated and user.is_staff
)
@require_POST
def admin_delete_movie(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()

    messages.success(request, 'Movie deleted successfully!')

    return redirect('admin_manage_movies')


# Manage Genres

@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
def admin_manage_genres(request):
    genres = Genre.objects.all().order_by('name')
    return render(request, 'admin_panel/manage_genres.html', {
        'genres': genres
    })


@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
def admin_add_genre(request):
    if request.method == 'POST':
        form = GenreForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Genre added successfully!')
            return redirect('admin_manage_genres')
    else:
        form = GenreForm()

    return render(request, 'admin_panel/add_genre.html', {
        'form': form
    })


@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
def admin_edit_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)

    if request.method == 'POST':
        form = GenreForm(request.POST, instance=genre)

        if form.is_valid():
            form.save()
            messages.success(request, 'Genre updated successfully!')
            return redirect('admin_manage_genres')
    else:
        form = GenreForm(instance=genre)

    return render(request, 'admin_panel/edit_genre.html', {
        'form': form,
        'genre': genre
    })


@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
@require_POST
def admin_delete_genre(request, genre_id):
    genre = get_object_or_404(Genre, id=genre_id)

    # Prevent deleting a genre that has movies
    if genre.movies.exists():
        messages.error(
            request,
            'Cannot delete this genre because movies are associated with it.'
        )
    else:
        genre.delete()
        messages.success(request, 'Genre deleted successfully!')

    return redirect('admin_manage_genres')



@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
def admin_manage_users(request):
    User = get_user_model()

    users = User.objects.all().order_by('-date_joined')

    return render(request, 'admin_panel/manage_users.html', {
        'users': users
    })



@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
@require_POST
def admin_toggle_user(request, user_id):
    User = get_user_model()

    selected_user = get_object_or_404(User, id=user_id)

    # Prevent admin from deactivating their own account
    if selected_user.id == request.user.id:
        messages.error(request, "You cannot change your own account status.")
        return redirect('admin_manage_users')

    selected_user.is_active = not selected_user.is_active
    selected_user.save()

    if selected_user.is_active:
        messages.success(request, f"{selected_user.username} activated successfully!")
    else:
        messages.success(request, f"{selected_user.username} deactivated successfully!")

    return redirect('admin_manage_users')



# Manage Reviews

@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
def admin_manage_reviews(request):
    reviews = Review.objects.select_related(
        'user', 'movie'
    ).all().order_by('-created_at')

    return render(request, 'admin_panel/manage_reviews.html', {
        'reviews': reviews
    })


@user_passes_test(lambda user: user.is_authenticated and user.is_staff)
@require_POST
def admin_delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    review.delete()

    messages.success(request, 'Review deleted successfully!')

    return redirect('admin_manage_reviews')



# ---------------------------------------------------
@login_required
@require_POST
def delete_my_review(request, review_id):
    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    review.delete()

    messages.success(request, "Your review was deleted successfully!")

    return redirect('my_reviews')


# ---------------------------------------------------------------------------

@login_required
def profile_view(request):

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            messages.success(request, "Your password has been changed successfully!")
            return redirect('profile')

    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'profile.html', {
        'form': form
    })