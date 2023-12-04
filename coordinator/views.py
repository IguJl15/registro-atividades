from typing import Any

from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.views.generic.list import ListView

from scholar.models import Scholar
from scholarship.models import Scholarship

from .access_mixins import CoordinatorRequiredMixin
from .forms import (
    AddressForm,
    BankingInfoForm,
    ExistingScholarForm,
    PersonalDataForm,
    ScholarForm,
)


class ScholarListView(CoordinatorRequiredMixin, ListView):
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


class ScholarCreateView(CoordinatorRequiredMixin, CreateView):
    model = Scholar
    form_class = ScholarForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        coordinator_scholarships: QuerySet = (
            self.request.user.scholar.coordinator.scholarship_set
        )

        # Get the selected scholarship
        selected_scholarship: Scholarship = form.cleaned_data["scholarship"]

        coordinator_projects = coordinator_scholarships.values_list(
            "project_id", flat=True
        )

        if selected_scholarship.project_id not in coordinator_projects:
            form.add_error("scholarship", "Você não tem acesso a esta bolsa")
            return self.form_invalid(form)
        
        instance: Scholar = form.save()
        # Add the selected scholarship to the new scholar
        instance.scholarship_set.add(selected_scholarship)

        return super().form_valid(form)

    def get_form_kwargs(self) -> dict[str, Any]:
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs

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


class ScholarCreateWithSearchView(CoordinatorRequiredMixin, CreateView):
    model = Scholar
    form_class = ExistingScholarForm
    template_name = "add_scholar_form.html"
    success_url = {"name": "scholars_list"}

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        cpf = form.cleaned_data["cpf"]

        found_scholar = Scholar.objects.filter(name__icontains=name, cpf=cpf).first()

        if found_scholar is None:
            form.add_error(
                None,
                "Não foi possível encontrar o bolsista",
            )

            return super().form_invalid(form)

        selected_scholarship: Scholarship = form.cleaned_data["scholarship"]

        coordinator_scholarships: QuerySet = (
            self.request.user.scholar.coordinator.scholarship_set
        )

        coordinator_projects = coordinator_scholarships.values_list(
            "project_id", flat=True
        )

        if selected_scholarship.project_id not in coordinator_projects:
            form.add_error("scholarship", "Você não tem acesso a esta bolsa")
            return self.form_invalid(form)

        if selected_scholarship in found_scholar.scholarship_set.all():
            form.add_error(
                "scholarship", "Este bolsista ja está cadastrado neste perfil de bolsa"
            )
            return self.form_invalid(form)

        found_scholar.scholarship_set.add(selected_scholarship)
        found_scholar.save()

        form.instance = found_scholar

        return redirect("scholars_list")

    def get_form_kwargs(self) -> dict[str, Any]:
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs
