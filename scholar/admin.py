from django.contrib import admin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from scholarship.models import Scholarship

from scholar.models import (
    Address,
    Bank,
    BankingInfo,
    CustomUser,
    InstitutionalSchedule,
    PersonalData,
    Scholar,
)


class ScholarInline(admin.StackedInline):
    model = Scholar
    can_delete = False

    exclude = ["address", "banking_info", "institutional_schedule", "personal_data"]


class UserAddressInline(admin.StackedInline):
    model = Address
    can_delete = False


class UserPersonalDataInline(admin.StackedInline):
    model = PersonalData
    can_delete = False


class UserBankingInfoInline(admin.StackedInline):
    model = BankingInfo
    can_delete = False


class UserInstitutionalScheduleInline(admin.TabularInline):
    model = InstitutionalSchedule
    can_delete = False


# class UserInline(admin.TabularInline):
#     form = UserCreationForm
#     model = User


@admin.register(Scholar)
class ScholarAdmin(admin.ModelAdmin):
    inlines = [
        UserAddressInline,
        UserPersonalDataInline,
        UserBankingInfoInline,
        UserInstitutionalScheduleInline,
    ]
    filter_horizontal = ['scholarship']
    exclude =[ 'user']


admin.site.register(Bank)
admin.site.register(CustomUser)