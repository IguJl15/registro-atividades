from django import forms
from scholar.models import PersonalData, BankingInfo, Address


class PersonalDataForm(forms.ModelForm):
    class Meta:
        model = PersonalData
        fields = "__all__"
        exclude = ['user']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"
        exclude = ['user']


class BankingInfoForm(forms.ModelForm):
    class Meta:
        model = BankingInfo
        fields = "__all__"
        exclude = ['user']
