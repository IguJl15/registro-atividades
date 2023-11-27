from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager

class CustomUser(AbstractUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True)

    # User details
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("bolsistas", kwargs={"pk": self.pk})
