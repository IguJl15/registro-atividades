from django.db import models
from django.urls import reverse



class Project(models.Model):
    name = models.CharField("Nome", max_length=150)
    campus = models.CharField("Campus", max_length=150)

    class Meta:
        verbose_name = "projeto"
        verbose_name_plural = "projetos"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("project_detail", kwargs={"pk": self.pk})


# Create your models here.
class Scholarship(models.Model):
    description = models.CharField("Descrição", max_length=50)
    value = models.DecimalField("Valor por hora", max_digits=6, decimal_places=2)

    project = models.ForeignKey(
        Project, verbose_name="Projeto", on_delete=models.PROTECT
    )

    scholarship_holders = models.ManyToManyField('scholarship_holder.ScholarshipHolder', verbose_name="Bolsistas")

    class Meta:
        verbose_name = "bolsa"
        verbose_name_plural = "bolsas"

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("bolsa", kwargs={"pk": self.pk})
