from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Scholar

class CoordinatorRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not authenticated
            return self.handle_no_permission()
        
        print("User dir")
        for field in dir(request.user):
            print(field)

        if not hasattr(request.user, 'scholar'):
            # User is authenticated but not a scholar
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)
