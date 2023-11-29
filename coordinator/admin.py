from django.contrib import admin
from .models import Coordinator
from scholar.admin import ScholarAdmin
    
# Register your models here.
admin.site.register(Coordinator, ScholarAdmin)