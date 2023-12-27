from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import RequestFactory
from django.http import JsonResponse

from movie.forms import CommentForm
from movie.models import Movie, Comment
from movie.views import (
    MovieListView,
    MovieDetailView,
    SearchResultsView,
    FavoritesView,
    ToggleFavoriteView,
    AddMovieView,
    UpdateMovieView,
    AddCommentView
)


class MovieTestCase(TestCase):

    def setUp(self):
        # Set up a user and a movie for testing
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(title='Test Movie', director='Test Director', genre='Test Genre')

    def test_movie_list_view(self):
        # Test MovieListView
        request = self.factory.get(reverse('movies:movie_list'))
        response = MovieListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')
        self.assertTemplateUsed(response, 'movie:movie_list.html')

    def test_movie_detail_view(self):
        # Test MovieDetailView
        request = self.factory.get(reverse('movies:movie_detail', args=[self.movie.id]))
        request.user = self.user
        response = MovieDetailView.as_view()(request, pk=self.movie.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')
        self.assertTemplateUsed(response, 'movie:movie_detail.html')

    def test_search_results_view(self):
        # Test SearchResultsView
        request = self.factory.get(reverse('movies:search_results'), {'q': 'Test'})
        response = SearchResultsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')
        self.assertTemplateUsed(response, 'movie:search_results.html')

    def test_favorites_view(self):
        # Test FavoritesView
        request = self.factory.get(reverse('movies:favorites'))
        request.user = self.user
        response = FavoritesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Movie')
        self.assertTemplateUsed(response, 'movie:favorite_movies.html')

    def test_toggle_favorite_view(self):
        # Test ToggleFavoriteView
        request = self.factory.post(reverse('movies:toggle_favorite', args=[self.movie.id]))
        request.user = self.user
        response = ToggleFavoriteView.as_view()(request, movie_id=self.movie.id)
        self.assertEqual(response.status_code, 200)
        data = JsonResponse(response.json())
        self.assertEqual(data['status'], 'success')
        self.assertTrue(data['is_favorite'])

    def test_add_movie_view(self):
        # Test AddMovieView
        data = {
            'title': 'New Movie',
            'director': 'New Director',
            'genre': 'New Genre',
        }
        request = self.factory.post(reverse('movies:add_movie'), data)
        request.user = self.user
        response = AddMovieView.as_view()(request)
        self.assertEqual(response.status_code, 302)  # Redirect after successful post
        self.assertTrue(Movie.objects.filter(title='New Movie').exists())
        self.assertTemplateUsed(response, 'movie:add_movie.html')

    def test_update_movie_view(self):
        # Test UpdateMovieView
        data = {
            'description': 'Updated Description',
            'release_date': '2023-01-01',
        }
        request = self.factory.post(reverse('movies:update_movie', args=[self.movie.id]), data)
        request.user = self.user
        response = UpdateMovieView.as_view()(request, pk=self.movie.id)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.description, 'Updated Description')
        self.assertTemplateUsed(response, 'movie:update_movie.html')


class AddCommentViewTestCase(TestCase):

    def setUp(self):
        # Set up a user and a movie for testing
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(title='Test Movie', director='Test Director', genre='Test Genre')

    def test_get_add_comment_view(self):
        # Test handling GET request for adding a new comment
        request = self.factory.get(reverse('movies:add_comment', args=[self.movie.id]))
        request.user = self.user
        response = AddCommentView.as_view()(request, pk=self.movie.id)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_comment.html')
        self.assertIsInstance(response.context_data['form'], CommentForm)
        self.assertEqual(response.context_data['movie'], self.movie)

    def test_post_add_comment_view(self):
        # Test handling POST request for adding a new comment
        data = {'text': 'Test Comment'}
        request = self.factory.post(reverse('movies:add_comment', args=[self.movie.id]), data)
        request.user = self.user
        response = AddCommentView.as_view()(request, pk=self.movie.id)
        self.assertEqual(response.status_code, 302)  # Redirect after successful post
        self.assertTrue(Comment.objects.filter(text='Test Comment', movie=self.movie, user=self.user).exists())
        self.assertRedirects(response, reverse('movies:movie_detail', args=[self.movie.id]))


class MostLikedMoviesViewTest(TestCase):
    def setUp(self):
        # Create test data for movies with ratings
        self.movie1 = Movie.objects.create(title='Movie 1')
        self.movie2 = Movie.objects.create(title='Movie 2')
        self.movie3 = Movie.objects.create(title='Movie 3')

        # Create test ratings for movies
        self.movie1.ratings.create(user=User.objects.create_user(username='user1'), rating=5)
        self.movie2.ratings.create(user=User.objects.create_user(username='user2'), rating=4)
        self.movie3.ratings.create(user=User.objects.create_user(username='user3'), rating=3)

    def test_most_liked_movies_view(self):
        url = reverse('most_liked_movies')
        response = self.client.get(url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the template is rendered
        self.assertTemplateUsed(response, 'movie_liked.html')

        # Check that the most_liked_movies context variable is passed to the template
        self.assertIn('most_liked_movies', response.context)

        # Check that the correct movies are in the most_liked_movies context variable
        most_liked_movies = response.context['most_liked_movies']
        self.assertEqual(len(most_liked_movies), 3)
        self.assertEqual(most_liked_movies[0], self.movie1)
        self.assertEqual(most_liked_movies[1], self.movie2)
        self.assertEqual(most_liked_movies[2], self.movie3)


class NewestMoviesViewTest(TestCase):
    def setUp(self):
        # Create test data for movies with release dates
        self.movie1 = Movie.objects.create(title='Movie 1', release_date='2022-01-01')
        self.movie2 = Movie.objects.create(title='Movie 2', release_date='2022-02-01')
        self.movie3 = Movie.objects.create(title='Movie 3', release_date='2022-03-01')

    def test_newest_movies_view(self):
        url = reverse('newest_movies')
        response = self.client.get(url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the template is rendered
        self.assertTemplateUsed(response, 'movie_newest.html')

        # Check that the newest_movies context variable is passed to the template
        self.assertIn('newest_movies', response.context)

        # Check that the correct movies are in the newest_movies context variable
        newest_movies = response.context['newest_movies']
        self.assertEqual(len(newest_movies), 3)
        self.assertEqual(newest_movies[0], self.movie3)
        self.assertEqual(newest_movies[1], self.movie2)
        self.assertEqual(newest_movies[2], self.movie1)


class GenreMoviesViewTest(TestCase):
    def setUp(self):
        # Create test data for movies with genres
        self.genre1 = Movie.objects.create(name='Genre 1')
        self.genre2 = Movie.objects.create(name='Genre 2')

        self.movie1 = Movie.objects.create(title='Movie 1', genre=self.genre1)
        self.movie2 = Movie.objects.create(title='Movie 2', genre=self.genre1)
        self.movie3 = Movie.objects.create(title='Movie 3', genre=self.genre2)

    def test_genre_movies_view(self):
        url = reverse('genre_movies')
        response = self.client.get(url)

        # Check that the response is successful
        self.assertEqual(response.status_code, 200)

        # Check that the template is rendered
        self.assertTemplateUsed(response, 'movie_genres.html')

        # Check that the genre_movies context variable is passed to the template
        self.assertIn('genre_movies', response.context)

        # Check that the correct movies are in the genre_movies context variable
        genre_movies = response.context['genre_movies']
        self.assertEqual(len(genre_movies), 2)
        self.assertIn(self.genre1, genre_movies)
        self.assertIn(self.genre2, genre_movies)

        # Check that the movies for each genre are correct
        self.assertEqual(len(genre_movies[self.genre1]), 2)
        self.assertEqual(len(genre_movies[self.genre2]), 1)
        self.assertIn(self.movie1, genre_movies[self.genre1])
        self.assertIn(self.movie2, genre_movies[self.genre1])
        self.assertIn(self.movie3, genre_movies[self.genre2])

