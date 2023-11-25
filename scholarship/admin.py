from django.contrib import admin

from scholarship.models import Project, Scholarship

class ScholarshipInline(admin.TabularInline):
    model = Scholarship
    # exclude = ['scholars']
    filter_horizontal = ['scholars']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ScholarshipInline]
    
