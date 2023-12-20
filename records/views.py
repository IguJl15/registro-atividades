from datetime import datetime, timedelta
from decimal import Decimal
from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, FormView
from wkhtmltopdf.views import PDFTemplateView, PDFTemplateResponse

from scholar.access_mixins import ScholarRequiredMixin
from scholar.models import Scholar
from scholarship.models import Scholarship

from .forms import RecordCreateForm, ReportCreateForm
from .models import Record


class RecordCreateView(ScholarRequiredMixin, CreateView):
    model = Record
    form_class = RecordCreateForm
    initial = {
        "date": datetime.now(),
        "start": "08:00",
        "end": "12:00",
    }

    def form_valid(self, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()

        if form.is_valid():
            # Retrieve the current scholar's ID
            current_scholar: Scholar = self.request.user.scholar

            selected_scholarship: Scholarship = form.cleaned_data["scholarship"]
            scholarship: set[Scholarship] = current_scholar.scholarship_set.get(
                id=selected_scholarship.id
            )
            if not scholarship:
                return self.form_invalid(form)
            # Create a new Record instance
            record = Record(
                description=form.cleaned_data["description"],
                date=form.cleaned_data["date"],
                start=form.cleaned_data["start"],
                end=form.cleaned_data["end"],
                scholar=current_scholar,
                scholarship=selected_scholarship,
            )

            # Save the Record instance
            record.save()

            # Redirect to the success page
            return redirect("records_home")

        return super().form_invalid(form)

    def get_form_kwargs(self) -> dict[str, Any]:
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs


class RecordDeleteView(ScholarRequiredMixin, DeleteView):
    model = Record
    success_url = "/registros"

    def get_queryset(self) -> QuerySet[Any]:
        current_scholar = self.request.user.scholar
        return Record.objects.filter(scholar=current_scholar)
    
class RecordUpdateView(ScholarRequiredMixin, UpdateView):
    model = Record
    form_class = RecordCreateForm
    success_url = "/registros"

    def get_queryset(self) -> QuerySet[Any]:
        current_scholar = self.request.user.scholar
        return Record.objects.filter(scholar=current_scholar)
    
    def get_form_kwargs(self) -> dict[str, Any]:
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs

class RecordListView(ScholarRequiredMixin, ListView):
    model = Record

    def get_queryset(self):
        # Filter records to only show the current user's scholar's records
        current_scholar = self.request.user.scholar
        project_id = self.request.GET.get("scholarship", None)

        queryset = Record.objects.filter(scholar=current_scholar).order_by("-date")

        if project_id:
            queryset = queryset.filter(scholarship__id__in=project_id)

        date = self.request.GET.get("date", None)

        if date:
            year = int(date.split("-")[0])
            month = int(date.split("-")[1])
            queryset = queryset.filter(date__month=month, date__year=year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["scholarships_list"] = self.request.user.scholar.scholarship_set.all()

        records: QuerySet = self.object_list

        context["total_hours"] = sum(
            [rec.ellapsed_time for rec in records], timedelta(0, 0, 0, 0, 0, 0, 0)
        )
        context["total_value"] = sum([rec.total_value for rec in records], Decimal(0))

        return context


class RecordReportView(RecordListView):
    template_name = "records_report.html"
    template_name_suffix = ""

class ReportFormView(FormView):
    template_name = "report_form.html"
    form_class = ReportCreateForm
    initial = {"date": datetime.now()}
    success_url = "/registros"

    def get_form_kwargs(self) -> dict[str, Any]:
        """Passes the request object to the form class.
        This is necessary to only display members that belong to a given user"""
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs
    
    
    def form_valid(self, form: form_class):
        current_scholar = self.request.user.scholar

        queryset = Record.objects.filter(scholar=current_scholar).order_by("-date")
        
        project_id = self.request.POST.get("scholarship", None)
        queryset = queryset.filter(scholarship__id__in=project_id)
        
        date = form.data["date"]
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])

        queryset = queryset.filter(date__month=month, date__year=year)

        context = self.get_context_data(records=queryset)

        response = PDFTemplateResponse(request=self.request,
                                       template="records_report.html",
                                       filename="relatorio_de_ativdades.pdf",
                                       context=context,
                                       show_content_in_browser=True,
                                       cmd_options={"enable-local-file-access": None, "verbose": None},
                                       )
        return response


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if "records" not in kwargs:
            return context
        
        records: QuerySet = kwargs["records"]
        
        context['object_list'] = records

        context["total_hours"] = sum(
            [rec.ellapsed_time for rec in records], timedelta(0, 0, 0, 0, 0, 0, 0)
        )
        context["total_value"] = sum([rec.total_value for rec in records], Decimal(0))

        return context

    
    def form_invalid(self, form: Any) -> HttpResponse:
        return self.form_valid(form)

class TestePdfView(PDFTemplateView):
    filename = None
    template_name = "records_report.html"
    options = {"enable-local-file-access": None, "verbose": None}

    def get_queryset(self):
        # Filter records to only show the current user's scholar's records
        current_scholar = self.request.user.scholar
        project_id = self.request.GET.get("scholarship", None)

        queryset = Record.objects.filter(scholar=current_scholar).order_by("-date")

        if project_id:
            queryset = queryset.filter(scholarship__id__in=project_id)

        date = self.request.GET.get("date", None)

        if date:
            year = int(date.split("-")[0])
            month = int(date.split("-")[1])
            queryset = queryset.filter(date__month=month, date__year=year)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context["scholarships_list"] = self.request.user.scholar.scholarship_set.all()

        records: QuerySet = context["object_list"]

        context["total_hours"] = sum(
            [rec.ellapsed_time for rec in records], timedelta(0, 0, 0, 0, 0, 0, 0)
        )
        context["total_value"] = sum([rec.total_value for rec in records], Decimal(0))

        return context
