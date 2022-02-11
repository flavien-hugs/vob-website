# page.managers.py

from django.db import models
from django.utils import timezone


class PageQuerySet(models.QuerySet):
    
    def active(self):
        return self.filter(
            is_active=True,
            created_at__lte=timezone.now()
        )


class PageQuerySetManager(models.Manager):
    
    def get_queryset(self):
        return PageQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()
