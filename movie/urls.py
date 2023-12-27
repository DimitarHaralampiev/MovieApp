from django.urls import path

from movie.views import (
    MovieListView,
    MovieDetailView,
    SearchResultsView,
    FavoritesView,
    AddMovieView,
    DeleteMovieView,
    UpdateMovieView,
    ToggleFavoriteView,
    AddCommentView,
    MostLikedMoviesView,
    NewestMoviesView,
    GenreMoviesView,
)

app_name = 'movies'

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'),
    path('<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('favorites/', FavoritesView.as_view(), name='favorite_movies'),
    path('add/', AddMovieView.as_view(), name='add_movie'),
    path('movie/<int:pk>/delete/', DeleteMovieView.as_view(), name='delete_movie'),
    path('movie/<int:pk>/update/', UpdateMovieView.as_view(), name='update_movie'),
    path('movie/<int:pk>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('toggle_favorite/<int:movie_id>/', ToggleFavoriteView.as_view(), name='toggle_favorite'),
    path('liked/', MostLikedMoviesView.as_view(), name='movie_liked'),
    path('newest/', NewestMoviesView.as_view(), name='movie_newest'),
    path('genres/', GenreMoviesView.as_view(), name='movie_genres'),
]
