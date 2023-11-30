from django import forms
from scholar.models import PersonalData, BankingInfo, Address, Scholar
from scholarship.models import Scholarship


class ScholarshipsChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, member):
        return f"{member.description} ({member.project.name})"


class ScholarForm(forms.ModelForm):
    scholarship = ScholarshipsChoiceField(
        queryset=Scholarship.objects.none(), empty_label=None, label="Bolsa"
    )

    class Meta:
        model = Scholar
        fields =  "__all__"
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")

        super().__init__(*args, **kwargs)

        current_coordinator: Scholar
        # If the scholar is not available, use the current user's scholar
        if self.request.user.scholar is not None:
            current_coordinator = self.request.user.scholar
            coordinator_projects = current_coordinator.scholarship_set.values_list(
                "project_id", flat=True
            )
            scholarships = Scholarship.objects.filter(project__in=coordinator_projects)
            self.fields["scholarship"].queryset = scholarships.order_by("project__name")


class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        fields = "__all__"
        exclude = ["user"]


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        exclude = ["user"]


class BankingInfoForm(forms.ModelForm):
    class Meta:
        model = BankingInfo
        fields = "__all__"
        exclude = ["user"]
