import re

from scholar.models import Scholar
from users.models import CustomUser


def create_custom_user_for_scholar(scholar: Scholar, created):
    if created:
        custom_user = CustomUser.objects.create_user(
            email=scholar.email, 
            password=re.sub("[-\. ]", "", scholar.cpf)
        )
        
        scholar.user = custom_user
        scholar.save()