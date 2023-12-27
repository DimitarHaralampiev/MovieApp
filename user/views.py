from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .forms import UserForm, UserProfileForm, UserLocationForm
from .models import UserProfile


class ProfileView(LoginRequiredMixin, View):
    """View for displaying and updating user profile information."""

    def get(self, request):
        """Handle GET request to display user profile."""
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            # Create UserProfile if it doesn't exist
            user_profile = UserProfile.objects.create(user=request.user)

        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
        location_form = UserLocationForm(instance=user_profile.location)

        return render(request, 'registrations/profile.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'location_form': location_form,
        })

    def post(self, request):
        """Handle POST request to update user profile."""
        user_profile = get_object_or_404(UserProfile, user=request.user)
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        location_form = UserLocationForm(request.POST, request.FILES, instance=user_profile.location)

        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('movies:movie_list')
        else:
            messages.error(request, 'Error updating profile!')
            return render(request, 'registrations/profile.html', {
                'user_form': user_form,
                'profile_form': profile_form,
                'location_form': location_form,
            })


class RegisterView(View):
    """View for user registration."""

    def get(self, request):
        """Handle GET request to display registration form."""
        register_form = UserCreationForm()
        return render(request, 'registrations/register.html', {'register_form': register_form})

    def post(self, request):
        """Handle POST request to process user registration."""
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            login(request, user)
            messages.success(request, f'User {user.username} registered successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'An error occurred while trying to register.')
            return render(request, 'registrations/register.html', {'register_form': register_form})


class LoginView(View):
    """View for user login."""

    def get(self, request):
        """Handle GET request to display login form."""
        login_form = AuthenticationForm()
        return render(request, 'registrations/login.html', {'login_form': login_form})

    def post(self, request):
        """Handle POST request to process user login."""
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'You are logged in as {username}.')
                return redirect('movies:movie_list')
        messages.error(request, 'An error occurred while trying to login.')
        return render(request, 'registrations/login.html', {'login_form': login_form})


@login_required
def logout_view(request):
    """View for user logout."""
    logout(request)
    return redirect('home')


def home_view(request):
    """View for displaying the home page."""
    return render(request, 'home.html')
