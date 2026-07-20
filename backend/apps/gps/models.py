from django.db import models

# Create your models here.
from django.db import models


class Device(models.Model):
    imei = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    last_seen = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.imei})"