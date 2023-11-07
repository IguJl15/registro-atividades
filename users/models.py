
import enum
from django.db import models
from django.urls import reverse

from cpf_field.models import CPFField
from phonenumber_field.modelfields import PhoneNumberField

class Bank(models.Model):
    code = models.CharField("Código")
    name = models.CharField("Nome")


    class Meta:
        verbose_name = "bank"
        verbose_name_plural = "banks"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("banks", kwargs={"pk": self.pk})


class BankingInfo(models.Model):
    class BankAccountType(models.TextChoices):
        CORRENTE = "CR", "Corrente"
        POUPANCA = "PP", "Poupança"

    type = models.CharField(
        max_length=2,
        choices=BankAccountType.choices
    )
    account_number = models.CharField()
    
    bank = models.ForeignKey("Bank", verbose_name="Banco", on_delete=models.PROTECT)
    agency_number = models.CharField()

    class Meta:
        abstract = True
        verbose_name = "Dados bancários"
        verbose_name_plural = "Dados bancários"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("bancos", kwargs={"pk": self.pk})

class Address(models.Model):
    postal_code = models.CharField(max_length=8, verbose_name="CEP")

    locality = models.CharField(verbose_name="Logradouro")
    number = models.CharField(verbose_name="Nº")

    state = models.CharField(verbose_name="Estado")



    class Meta:
        abstract = True
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Address_detail", kwargs={"pk": self.pk})

class PersonalData(models.Model):
    rg = models.CharField(verbose_name="RG")
    email = models.EmailField()
    phone = PhoneNumberField(verbose="Telefone")
    birthday = models.DateTimeField("Nascimento")

    class Meta:
        abstract = True
        verbose_name = "Dados pessoais"
        verbose_name_plural = "Dados pessoais"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("PersonalData_detail", kwargs={"pk": self.pk})
 

# Create your models here.
class ScholarshipHolder(models.Model):
    cpf =  CPFField(verbose_name='CPF', primary_key=True)

    name = models.CharField(verbose_name='Nome')


    banking_info = models.OneToOneField(BankingInfo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Bolsista"
        verbose_name_plural = "Bolsistas"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("bolsistas", kwargs={"pk": self.pk})
