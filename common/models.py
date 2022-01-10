# common.models.py

import uuid

from django.db import models
from django.contrib import admin
from django.utils import timezone


NULL_AND_BLANK = {
    'null': True,
    'blank': True
}

class BaseTimeStampModel(models.Model):
    
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDSlugMixin(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid'
    )
    slug = models.SlugField(
        unique=True,
        editable=False,
        verbose_name='slug',
        help_text='Automatiquement formé à partir du nom.',
        **NULL_AND_BLANK
    )

    class Meta:
        abstract = True


class StatusAndPublishedMixin(models.Model):
    
    P = 'Publié'
    E = 'En Attente'

    STATUS_CHOICES = (
        (P, 'Publié'),
        (E, 'En Attente')
    )

    status = models.CharField(
        default=E,
        max_length=10,
    	verbose_name="status",
    	choices=STATUS_CHOICES,
        help_text="status."
    )
    published = models.DateTimeField(
        auto_now_add=False, auto_now=False,
        verbose_name='date et de publication',
        help_text="Programmé la date et l'heure de la formation."
    )

    class Meta:
        abstract = True

    def clean(self):
        if (
            self.published >= self.date_of_course
        ):
            raise ValidationError(
                {
                    "published": "La date de publication ne doit pas \
                    être supérieure ou égale à la date de début de formation."
                }
            )
