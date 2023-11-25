import re
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Scholar, CustomUser


@receiver(post_save, sender=Scholar)
def create_custom_user_for_scholar(sender, instance: Scholar, created, **kwargs):
    if created:
        custom_user = CustomUser.objects.create_user(
            email=instance.email, 
            password=re.sub("[-\. ]", "", instance.cpf)
        )

        instance.user = custom_user
        instance.save()
