from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.list import ListView

from scholar.models import Scholar

# Create your views here.
class ScholarListView(ListView):
    model = Scholar

    def get_queryset(self) -> QuerySet[Any]:
        coordinator = self.request.user
        coordinator_projects = coordinator.scholarships.values_list("project_id", flat=True)
        scholars = Scholar.objects.filter(scholarships__project__in=coordinator_projects)
        
        return scholars
