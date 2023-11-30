from django.db.models.signals import post_save
from django.dispatch import receiver

from users.signals_functions import create_custom_user_for_scholar

from .models import Scholar


@receiver(post_save, sender=Scholar)
def create_custom_user(sender, instance: Scholar, created, **kwargs):
    create_custom_user_for_scholar(instance, created)