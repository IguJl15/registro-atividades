from django.contrib import admin

from scholar.models import (
    Address,
    Bank,
    BankingInfo,
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


class ScholarAdmin(admin.ModelAdmin):
    inlines = [
        UserAddressInline,
        UserPersonalDataInline,
        UserBankingInfoInline,
        UserInstitutionalScheduleInline,
    ]
    filter_horizontal = ["scholarship"]
    exclude = ["user"]


admin.site.register(Scholar, ScholarAdmin)
admin.site.register(Bank)
