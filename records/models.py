from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

from django.db import models

from scholar.models import Scholar
from scholarship.models import Scholarship

class Record(models.Model):
    description = models.CharField("Descrição", max_length=250)

    date = models.DateField("Data", auto_now=False, auto_now_add=False)

    start = models.TimeField("Hora inicial", auto_now=False, auto_now_add=False)
    end = models.TimeField("Hora final", auto_now=False, auto_now_add=False)

    scholar = models.ForeignKey(Scholar, on_delete=models.PROTECT)
    scholarship = models.ForeignKey(Scholarship, on_delete=models.PROTECT)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "registro de atividade"
        verbose_name_plural = "registros de atividades"

    @property
    def total_value(self):
        return self.scholarship.value * Decimal(
            self.ellapsed_time.total_seconds() / 3600
        )

    @property
    def ellapsed_time(self):
        # https://stackoverflow.com/questions/21774302/how-do-i-calculate-the-time-difference-in-a-django-template
        dummydate = date(2000, 1, 1)  # Needed to convert time to a datetime object
        dt1 = datetime.combine(dummydate, self.start)
        dt2 = datetime.combine(dummydate, self.end)

        return dt2 - dt1

    @property
    def can_delete(self):
        if not self.created:
            return True
        
        days_since_today: timedelta = datetime.now(timezone.utc) - self.created
        
        return days_since_today.days <= 30

    def __str__(self):
        return self.description
