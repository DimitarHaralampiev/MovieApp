from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import DatabaseError
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, UpdateView

from movie.forms import MovieForm, CommentForm, RatingForm
from movie.models import Movie, Comment, Rating


class MovieListView(ListView):
    """View for displaying a list of movies."""
    model = Movie
    template_name = 'movie_list.html'
    context_object_name = 'movies'

    def get_context_data(self, **kwargs):
        """Get additional context data for rendering the movie list."""
        context = super().get_context_data(**kwargs)
        context['genre_choices'] = Movie._meta.get_field('genre').choices
        return context

    def get_queryset(self):
        """Get the queryset of movies based on genre filter."""
        genre_filter = self.request.GET.get('genre')
        if genre_filter:
            return Movie.objects.filter(genre=genre_filter)
        else:
            return Movie.objects.all()


class MostLikedMoviesView(View):
    """View to display the top 5 most liked movies."""
    template_name = 'movie_liked.html'

    def get(self, request, *args, **kwargs):
        """Handles HTTP GET requests and renders the template with the most liked movies data."""
        most_liked_movies = Movie.objects.annotate(num_ratings=Count('ratings')).order_by('-num_ratings')[:5]

        return render(request, self.template_name, {
            'most_liked_movies': most_liked_movies,
        })


class NewestMoviesView(View):
    """View to display the top 5 newest movies."""
    template_name = 'movie_newest.html'

    def get(self, request, *args, **kwargs):
        """Handles HTTP GET requests and renders the template with the newest movies data."""
        newest_movies = Movie.objects.order_by('-release_date')[:5]

        return render(request, self.template_name, {
            'newest_movies': newest_movies,
        })


class GenreMoviesView(View):
    """View to display the last 5 movies for each genre with at least one movie."""
    template_name = 'movie_genres.html'

    def get(self, request, *args, **kwargs):
        """Handles HTTP GET requests and renders the template with the genre movies data."""
        genres_with_movies = set(Movie.objects.values_list('genre', flat=True).distinct())

        # Get last 5 movies for each genre with at least one movie
        genre_movies = {}
        for genre in genres_with_movies:
            genre_movies[genre] = Movie.objects.filter(genre=genre).order_by('-release_date')[:5]

        return render(request, self.template_name, {
            'genre_movies': genre_movies,
        })


class MovieDetailView(LoginRequiredMixin, DetailView):
    """View for displaying details and rating of a movie."""
    model = Movie
    template_name = 'movie_details.html'
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        """Get additional context data for rendering the movie details."""
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(movie=self.object)
        context['rating_form'] = RatingForm()
        return context

    def post(self, request, *args, **kwargs):
        """Handle POST request for submitting a movie rating."""
        movie = self.get_object()
        form = RatingForm(request.POST)
        try:
            if form.is_valid():
                # Check if the user has already submitted a rating for this movie
                existing_rating = Rating.objects.filter(movie=movie, user=request.user).first()

                if existing_rating:
                    # If the user has already submitted a rating, show an error message
                    messages.error(request, 'You have already submitted a rating for this movie.')
                else:
                    # Save the new rating
                    rating = form.save(commit=False)
                    rating.movie = movie
                    rating.user = request.user
                    rating.save()

                    # Add a success message for rating submission
                    messages.success(request, 'Rating submitted successfully')

            return redirect('movies:movie_detail', pk=movie.pk)

        except Exception as e:
            # Add an error message for the user in case of rating submission failure
            messages.error(request, 'An error occurred during rating submission')
            return redirect('movies:movie_detail', pk=movie.pk)


class SearchResultsView(View):
    """View for searching movies based on a query."""
    template_name = 'search_results.html'

    def get(self, request, *args, **kwargs):
        """Handle GET request for searching movies."""
        try:
            query = request.GET.get('q')
            genre_filter = request.GET.get('genre')
            movies = Movie.objects.filter(genre=genre_filter)

            if query:
                movies = movies.filter(
                    Q(title__icontains=query) | Q(director__icontains=query) | Q(director__icontains=query)
                )
                if movies.count() < 1:
                    return render(request, 'search_results.html', {'message': 'No movies found!'})
        except DatabaseError as e:
            # Display an error message in case of a database error
            return render(request, 'error/error.html', {'message': 'An error occurred while querying the database.'})
        else:
            return render(request, self.template_name, {'movies': movies, 'query': query})


class FavoritesView(ListView):
    """View for displaying a list of favorite movies."""
    model = Movie
    template_name = 'favorite_movies.html'
    context_object_name = 'favorite_movies'

    def get_queryset(self):
        """Get the queryset for favorite movies."""
        return Movie.objects.filter(is_favorite=True)


class ToggleFavoriteView(View):
    """View for toggling the favorite status of a movie."""

    def post(self, request, movie_id):
        """Handle POST request for toggling favorite status."""
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.is_favorite = not movie.is_favorite
        movie.save()
        return JsonResponse({'status': 'success', 'is_favorite': movie.is_favorite})


class AddMovieView(LoginRequiredMixin, View):
    """View for adding a new movie."""
    form_class = MovieForm
    template_name = 'add_movie.html'

    def get(self, request, *args, **kwargs):
        """Handle GET request for adding a new movie."""
        form = MovieForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Handle POST request for adding a new movie."""
        form = MovieForm(request.POST, request.FILES)
        try:
            if form.is_valid():
                if request.user.is_authenticated:
                    movie = form.save(commit=False)
                    movie.user = request.user
                    movie.save()
                    messages.success(request, 'Movie added successfully!')
                    return redirect('movies:movie_list')
                else:
                    # Display an error message if the user is not authenticated
                    messages.error(request, 'You must be logged in to add a movie.')
            else:
                # Display an error message if the form is not valid
                messages.error(request, 'Form is not valid. Please check the input.')
        except ValueError as e:
            # Display an error message if there is an issue processing the file upload
            messages.error(request, 'Error processing the file upload.')
        return render(request, self.template_name, {'form': form})


class UpdateMovieView(LoginRequiredMixin, UpdateView):
    """View for updating the details of a movie."""
    model = Movie
    fields = ['description', 'release_date', 'cover_image']
    template_name = 'update_movie.html'
    success_url = reverse_lazy('movies:movie_list')

    def form_valid(self, form):
        """Handle form validation for updating a movie."""
        messages.success(self.request, 'Movie updated successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        """Handle form validation failure for updating a movie."""
        messages.error(self.request, 'Error updating movie. Please check the form.')
        return super().form_invalid(form)


class DeleteMovieView(LoginRequiredMixin, DeleteView):
    """View for deleting a movie."""
    model = Movie
    success_url = reverse_lazy('movies:movie_list')


class AddCommentView(View):
    """View for adding a new comment to a movie."""
    template_name = 'add_comment.html'

    def get(self, request, pk):
        """Handle GET request for adding a new comment."""
        movie = get_object_or_404(Movie, pk=pk)
        form = CommentForm()
        return render(request, self.template_name, {'form': form, 'movie': movie})

    def post(self, request, pk):
        """Handle POST request for adding a new comment."""
        movie = get_object_or_404(Movie, pk=pk)
        form = CommentForm(request.POST)
        try:
            if form.is_valid():
                comment = form.save(commit=False)
                comment.movie = movie
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment submitted successfully')
                return redirect('movies:movie_detail', pk=pk)
        except Exception as e:
            # Add an error message for the user in case of comment submission failure
            messages.error(request, 'An error occurred during comment submission.')

        return render(request, self.template_name, {'form': form, 'movie': movie})



