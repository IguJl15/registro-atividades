from django.db import models
from django.urls import reverse
from scholarship.models import Scholarship

from scholarship_holder.models import ScholarshipHolder


class Record(models.Model):
    description = models.CharField("Descrição", max_length=250)

    date = models.DateField("Data", auto_now=False, auto_now_add=False)

    start = models.TimeField("Hora inicial", auto_now=False, auto_now_add=False)
    end = models.TimeField("Hora final", auto_now=False, auto_now_add=False)

    scholarship_holder = models.ForeignKey(ScholarshipHolder, verbose_name="Bolsista", on_delete=models.PROTECT)
    scholarship = models.ForeignKey(Scholarship, verbose_name="Bolsa", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "registro"
        verbose_name_plural = "registros"

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("registros", kwargs={"pk": self.pk})
