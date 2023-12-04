from django.db import models


class Project(models.Model):
    name = models.CharField("Nome", max_length=150)
    campus = models.CharField("Campus", max_length=150)

    class Meta:
        verbose_name = "projeto"
        verbose_name_plural = "projetos"

    def __str__(self):
        return self.name


# Create your models here.
class Scholarship(models.Model):
    description = models.CharField("Descrição", max_length=50)
    value = models.DecimalField("Valor por hora", max_digits=6, decimal_places=2)

    project = models.ForeignKey(Project, on_delete=models.PROTECT)

    scholars = models.ManyToManyField("scholar.Scholar", blank=True)

    class Meta:
        verbose_name = "perfil de bolsa"
        verbose_name_plural = "perfis de bolsas"

    def __str__(self):
        return self.description
