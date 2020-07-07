from django.db import models
from django.conf import settings


class Customer(models.Model):
    name = models.CharField(max_length=30, blank=False)
    surname = models.CharField(max_length=50, blank=False)
    photo = models.FileField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="customers_created", null=False, on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="customers_updated", null=True, on_delete=models.PROTECT)
