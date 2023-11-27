from typing import Any

from django.db.models import QuerySet
from django.forms import ModelChoiceField, ModelForm, TimeInput
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView

from records.models import Record
from scholar.access_mixins import ScholarRequiredMixin
from scholar.models import Scholar
from scholarship.models import Scholarship


class ScholarshipsChoiceField(ModelChoiceField):
    def label_from_instance(self, member):
        return f"{member.description} ({member.project.name})"


class RecordCreateForm(ModelForm):
    scholarship = ScholarshipsChoiceField(
        queryset=Scholarship.objects.none(), empty_label=None, label="Bolsa"
    )

    class Meta:
        model = Record
        fields = ["description", "date", "start", "end", "scholarship"]
        widgets = {"start": TimeInput(), "end": TimeInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

        current_scholar: Scholar
        # If the scholar is not available, use the current user's scholar
        if self.request.user.scholar is not None:
            current_scholar = self.request.user.scholar
            # Limit the scholarship choices to the current user's scholar's scholarships
            scholarships: QuerySet = current_scholar.scholarship_set.all()
            self.fields["scholarship"].queryset = scholarships.order_by("project__name")


class RecordCreateView(ScholarRequiredMixin, CreateView):
    model = Record
    form_class = RecordCreateForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.get_form()

        if form.is_valid():
            # Retrieve the current scholar's ID
            current_scholar: Scholar = request.user.scholar

            scholarships: set[Scholarship] = current_scholar.scholarship_set.all()
            # Create a new Record instance
            record = Record(
                description=form.cleaned_data["description"],
                date=form.cleaned_data["date"],
                start=form.cleaned_data["start"],
                end=form.cleaned_data["end"],
                scholar=current_scholar,
                scholarship=form.cleaned_data["scholarship"],
            )

            # Save the Record instance
            record.save()

            # Redirect to the success page
            return redirect("records_home")

        return self.form_invalid(form)

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
        project_id = self.request.GET.get('scholarship', None)

        if project_id:
            queryset = Record.objects.filter(scholar=current_scholar, scholarship__id__in=project_id)
        else:
            queryset = Record.objects.filter(scholar=current_scholar)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['scholarships_list'] = Scholarship.objects.filter(id__in=self.request.user.scholar.scholarship_set.all())
        return context