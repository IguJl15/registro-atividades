from django.contrib import admin

from scholarship.models import Project, Scholarship

class ScholarshipInline(admin.TabularInline):
    model = Scholarship
    # exclude = ['scholarship_holders']
    filter_horizontal = ['scholarship_holders']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ScholarshipInline]
    
