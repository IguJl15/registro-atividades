from django.contrib.auth.mixins import LoginRequiredMixin

class CoordinatorRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            # User is not authenticated
            return self.handle_no_permission()

        if (not hasattr(request.user, 'scholar')) or (not hasattr(request.user.scholar, 'coordinator')):
            # User is authenticated but not a coordinator
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs)
