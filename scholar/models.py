from django.db import models
from django.urls import reverse

from users.models import CustomUser


class Scholar(models.Model):
    user = models.OneToOneField(
        CustomUser,
        verbose_name="Usuário",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(verbose_name="Nome", max_length=250)
    email = models.EmailField("Email", unique=True)

    cpf = models.CharField(verbose_name="CPF", max_length=14)

    # scholarships = models.ManyToManyField("scholarship.Scholarship", verbose_name="Bolsas")

    class Meta:
        verbose_name = "bolsista"
        verbose_name_plural = "bolsistas"

    def __str__(self):
        return self.name


class Weekday(models.TextChoices):
    MONDAY = "0", "Segunda-Feira"
    TUESDAY = "1", "Terça-Feira"
    WEDNESDAY = "2", "Quarta-Feira"
    THURSDAY = "3", "Quinta-Feira"
    FRIDAY = "4", "Sexta-Feira"
    SATURDAY = "5", "Sábado"
    SUNDAY = "6", "Domingo"


class InstitutionalSchedule(models.Model):
    user = models.ForeignKey(Scholar, on_delete=models.CASCADE)

    week_day = models.CharField("dia", max_length=2, choices=Weekday.choices)

    start = models.TimeField("Hora inicial", auto_now=False, auto_now_add=False)
    end = models.TimeField("Hora final", auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = "horário institucional"
        verbose_name_plural = "horários institucionais"

    def __str__(self):
        return f"{self.week_day}: {self.start}:{self.end}"


class Bank(models.Model):
    ispb = models.CharField("ISPB", max_length=10)
    code = models.IntegerField("Código", null=True)
    name = models.CharField("Nome", max_length=150)

    class Meta:
        verbose_name = "banco"
        verbose_name_plural = "bancos"

    def __str__(self):
        return self.name


class BankingInfo(models.Model):
    class BankAccountType(models.TextChoices):
        CORRENTE = "CR", "Corrente"
        POUPANCA = "PP", "Poupança"

    user = models.OneToOneField(Scholar, on_delete=models.CASCADE)

    type = models.CharField("tipo", max_length=2, choices=BankAccountType.choices)
    account_number = models.CharField("número da conta", max_length=50)

    bank = models.ForeignKey(Bank, on_delete=models.PROTECT)
    agency_number = models.CharField("agência", max_length=10)

    class Meta:
        verbose_name = "dados bancários"
        verbose_name_plural = "dados bancários"

    def __str__(self):
        return self.account_number


class Address(models.Model):
    user = models.OneToOneField(Scholar, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=8, verbose_name="CEP")

    locality = models.CharField(
        verbose_name="logradouro", name="street", max_length=250
    )
    number = models.CharField(verbose_name="Número ou apt", max_length=10)

    state = models.CharField(verbose_name="Estado", max_length=250)

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return self.postal_code


class PersonalData(models.Model):
    user = models.OneToOneField(Scholar, on_delete=models.CASCADE)
    rg = models.CharField(verbose_name="RG", unique=True, max_length=100)
    phone = models.CharField("Telefone", max_length=50)
    birthday = models.DateField("data de nascimento")

    class Meta:
        verbose_name = "Dados pessoais"
        verbose_name_plural = "Dados pessoais"

    def __str__(self):
        return self.rg
