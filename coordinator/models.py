from django.db import models
from scholar.models import Scholar


class Coordinator(Scholar):
    is_coordinator = models.BooleanField("Coordenador", default=True)

    class Meta:
        verbose_name = "coordenador"
        verbose_name_plural = "coordenadores"

    def __str__(self):
        return f"{self.name} (Coordenador)"
