from django import forms
from django.db.models import QuerySet

from records.models import Record
from scholar.models import Scholar
from scholarship.models import Scholarship


class ScholarshipsChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, member):
        return f"{member.description} ({member.project.name})"


class RecordCreateForm(forms.ModelForm):
    scholarship = ScholarshipsChoiceField(
        queryset=Scholarship.objects.none(), empty_label=None, label="Bolsa"
    )

    class Meta:
        model = Record
        fields = ["description", "date", "start", "end", "scholarship"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "date"}),
            "start": forms.TimeInput(attrs={"type": "time"}),
            "end": forms.TimeInput(attrs={"type": "time"}),
        }

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

    def is_valid(self) -> bool:
        start = self.data["start"]
        end = self.data["end"]

        if end < start:
            self.add_error("end", "A Hora final deve ser depois da Hora inicial")
            return False

        return super().is_valid()
