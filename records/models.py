from datetime import date, datetime
import decimal
from django.db import models
from django.urls import reverse
from django.utils.timesince import timesince

from scholarship.models import Scholarship

from scholar.models import Scholar


class Record(models.Model):
    description = models.CharField("Descrição", max_length=250)

    date = models.DateField("Data", auto_now=False, auto_now_add=False)

    start = models.TimeField("Hora inicial", auto_now=False, auto_now_add=False)
    end = models.TimeField("Hora final", auto_now=False, auto_now_add=False)

    scholar = models.ForeignKey(Scholar, verbose_name="Bolsista", on_delete=models.PROTECT)
    scholarship = models.ForeignKey(Scholarship, verbose_name="Bolsa", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "registro"
        verbose_name_plural = "registros"
    
    @property
    def total_value(self):
        return self.scholarship.value * decimal.Decimal((self.ellapsed_time.total_seconds() / 3600))


    @property
    def ellapsed_time(self):
        # https://stackoverflow.com/questions/21774302/how-do-i-calculate-the-time-difference-in-a-django-template
        dummydate = date(2000,1,1)  # Needed to convert time to a datetime object
        dt1 = datetime.combine(dummydate, self.start)
        dt2 = datetime.combine(dummydate, self.end)

        return dt2 - dt1

    @property
    def formatted_ellapsed_time(self):
        return 

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse("registros", kwargs={"pk": self.pk})
