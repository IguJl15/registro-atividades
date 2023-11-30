from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import CreateView
from django.views.generic.list import ListView

from scholar.models import Scholar

from .forms import AddressForm, BankingInfoForm, PersonalDataForm


class ScholarListView(ListView):
    model = Scholar

    def get_queryset(self) -> QuerySet[Any]:
        coordinator = self.request.user.scholar.coordinator
        coordinator_projects = coordinator.scholarship_set.values_list(
            "project_id", flat=True
        )
        scholars = Scholar.objects.filter(
            scholarship__project__in=coordinator_projects
        ).exclude(id=coordinator.id)

        return scholars


class ScholarCreateView(CreateView):
    model = Scholar

    fields = ["name", "email", "cpf"]

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["address_form"] = AddressForm(
            self.request.POST if self.request.POST else None
        )
        context["personal_data_form"] = PersonalDataForm(
            self.request.POST if self.request.POST else None
        )
        context["banking_info_form"] = BankingInfoForm(
            self.request.POST if self.request.POST else None
        )

        return context
