from django.urls import path

from user.views import LoginView, RegisterView, logout_view, home_view, ProfileView

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', logout_view, name='logout'),
]