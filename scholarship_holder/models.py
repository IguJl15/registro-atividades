from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.urls import reverse

from .managers import CustomUserManager


class ScholarshipHolder(AbstractUser, PermissionsMixin):

    name = models.CharField(verbose_name="Nome", max_length=250)
    email = models.EmailField("Email", unique=True)

    cpf = models.CharField(verbose_name="CPF", max_length=14)

    # scholarships = models.ManyToManyField("scholarship.Scholarship", verbose_name="Bolsas")

    # User details
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "bolsista"
        verbose_name_plural = "bolsistas"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("bolsistas", kwargs={"pk": self.pk})


class Weekday(models.TextChoices):
    MONDAY = "0", "Segunda-Feira"
    TUESDAY = "1", "Terça-Feira"
    WEDNESDAY = "2", "Quarta-Feira"
    THURSDAY = "3", "Quinta-Feira"
    FRIDAY = "4", "Sexta-Feira"
    SATURDAY = "5", "Sábado"
    SUNDAY = "6", "Domingo"


class InstitutionalSchedule(models.Model):
    user = models.ForeignKey(ScholarshipHolder, on_delete=models.CASCADE)

    week_day = models.CharField(max_length=2, choices=Weekday.choices)

    start = models.TimeField("Hora inicial", auto_now=False, auto_now_add=False)
    end = models.TimeField("Hora final", auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "Horário Institucional"
        verbose_name_plural = "Horários Institucionais"

    def __str__(self):
        return f"{self.week_day}: {self.start}:{self.end}"

    def get_absolute_url(self):
        return reverse("InstitutionalSchedule_detail", kwargs={"pk": self.pk})


class Bank(models.Model):
    ispb = models.CharField("ISPB", max_length=10)
    code = models.IntegerField("Código", null=True)
    name = models.CharField("Nome", max_length=150)

    class Meta:
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("banks", kwargs={"pk": self.pk})


class BankingInfo(models.Model):
    class BankAccountType(models.TextChoices):
        CORRENTE = "CR", "Corrente"
        POUPANCA = "PP", "Poupança"

    user = models.OneToOneField(ScholarshipHolder, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=BankAccountType.choices)
    account_number = models.CharField(max_length=50)

    bank = models.ForeignKey(Bank, verbose_name="Banco", on_delete=models.PROTECT)
    agency_number = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Dados bancários"
        verbose_name_plural = "Dados bancários"

    def __str__(self):
        return self.account_number

    def get_absolute_url(self):
        return reverse("bancos", kwargs={"pk": self.pk})


class Address(models.Model):
    user = models.OneToOneField(ScholarshipHolder, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=8, verbose_name="CEP")

    locality = models.CharField(
        verbose_name="Logradouro", name="street", max_length=250
    )
    number = models.CharField(verbose_name="Nº", max_length=10)

    state = models.CharField(verbose_name="Estado", max_length=250)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return self.postal_code

    def get_absolute_url(self):
        return reverse("Address_detail", kwargs={"pk": self.pk})


class PersonalData(models.Model):
    user = models.OneToOneField(ScholarshipHolder, on_delete=models.CASCADE)
    rg = models.CharField(verbose_name="RG", unique=True, max_length=100)
    phone = models.CharField("Telefone", max_length=50)
    birthday = models.DateField("Nascimento")

    class Meta:
        verbose_name = "Dados pessoais"
        verbose_name_plural = "Dados pessoais"

    def __str__(self):
        return self.rg

    def get_absolute_url(self):
        return reverse("PersonalData_detail", kwargs={"pk": self.pk})
