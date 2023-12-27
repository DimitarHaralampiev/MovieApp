from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal receiver function that creates a user profile when a new User instance is created."""
    # Create a new UserProfile associated with the newly created User
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Signal receiver function that saves the user profile when a User instance is saved."""
    # Save the associated UserProfile when the User instance is saved
    instance.userprofile.save()