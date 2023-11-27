from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Scholar

class ScholarRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not authenticated
            return self.handle_no_permission()
        
        if not hasattr(request.user, 'scholar'):
            # User is authenticated but not a scholar
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)
