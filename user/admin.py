from django.contrib import admin

from user.models import UserProfile, LocationUser

admin.site.register(UserProfile)
admin.site.register(LocationUser)
