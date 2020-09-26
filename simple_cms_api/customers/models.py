from django.db import models
from django.conf import settings
from uuid import uuid4

class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


def rename_file(instance, filename):
    file_extension = filename.split('.')[-1]

    return f'{settings.MEDIA_URL}/{uuid4().hex}.{file_extension}'


class Customer(models.Model):
    name = models.CharField(max_length=30, blank=False)
    surname = models.CharField(max_length=50, blank=False)
    photo = models.FileField(upload_to=rename_file, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="customers_created", null=False, on_delete=models.PROTECT)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="customers_updated", null=True, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    objects = CustomerManager()
