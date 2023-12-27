from django.contrib.auth import get_user_model


def user_directory_path(instance, filename):
    """
        Generate the file path for uploading files based on the user.

        This function is used as the `upload_to` argument in FileField or ImageField of a model.
        It creates a directory structure based on the user's ID and organizes files within that structure.

        Parameters:
        - instance: An instance of the model to which the FileField or ImageField belongs.
                    It is typically an instance of a model that has a user attribute.
        - filename: The original filename of the uploaded file.

        Returns:
        - str: The file path in the format 'uploads/user_{user_id}/{filename}', where {user_id}
               is the ID of the user associated with the instance. If the user is not available
               or if there is an issue obtaining the user ID, 'unknown' is used as the user ID.

        Example:
        - If instance.user.id is 42 and the filename is 'profile_picture.jpg',
          the function will return 'uploads/user_42/profile_picture.jpg'.
        - If the user is not available or there is an issue obtaining the user ID,
          the function will return 'uploads/user_unknown/profile_picture.jpg'.
        """
    # Use get_user_model() instead of User for better compatibility
    User = get_user_model()

    # Assuming instance has a user attribute
    user_id = instance.user.id if instance.user else 'unknown'

    return f'uploads/user_{user_id}/{filename}'