# common.models.py

import uuid

from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.core.validators import RegexValidator

from embed_video.fields import EmbedVideoField

NULL_AND_BLANK = {
    'null': True,
    'blank': True
}


class BaseTimeStampModel(models.Model):

    created_at = models.DateTimeField(
        verbose_name='date de création',
        db_index=True, default=timezone.now
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @admin.display(description="date d'ajout")
    def date(self):
        return self.created_at.date()


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
        max_length=225,
        verbose_name='slug',
        help_text='Automatiquement formé à partir du nom.',
        **NULL_AND_BLANK
    )

    class Meta:
        abstract = True


class StatusAndPublishedMixin(models.Model):

    published = models.DateTimeField(
        default=timezone.now,
        auto_now_add=False, auto_now=False,
        verbose_name='date et de publication',
        help_text="Programmé la date et l'heure de la formation."
    )

    class Meta:
        abstract = True

    @admin.display(description="publié le")
    def date_published(self):
        return self.published.date()


class VideoDescription(models.Model):

    video = EmbedVideoField(
        verbose_name='vidéo (optionnelle)',
        help_text="Ajouté un lien d'une vidéo.",
        **NULL_AND_BLANK
    )

    class Meta:
        abstract = True


class UserBaseInfo(models.Model):

    class Meta:
        abstract = True

    email = models.EmailField(
        max_length=80,
        verbose_name='adresse de messagerie',
        **NULL_AND_BLANK
    )
    first_name = models.CharField(
        verbose_name='nom',
        max_length=80
    )
    last_name = models.CharField(
        verbose_name='prénom',
        max_length=80
    )
    phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex='^\+?1?\d{9,15}$',
                message="Le numéro de téléphone doit être saisi dans le format\
                '+225'. Jusqu'à 10 chiffres sont autorisés.",
                code='invalid_phone_number'
            ),
        ],
        verbose_name='téléphone',
    )
    phone_two = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex='^\+?1?\d{9,15}$',
                message="Le numéro de téléphone doit être saisi dans le format\
                '+225'. Jusqu'à 10 chiffres sont autorisés.",
                code='invalid_phone_number'
            ),
        ],
        verbose_name='téléphone 2 (facultatif)',
        **NULL_AND_BLANK
    )
    city = models.CharField(
        default="Bouaké",
        verbose_name='ville',
        max_length=80
    )
    country = models.CharField(
        default="Côte d'Ivoire",
        verbose_name='pays',
        max_length=80,
        **NULL_AND_BLANK
    )
    address = models.CharField(
        verbose_name='adresse de livraison',
        max_length=180,
    )

    @admin.display(description="nom & prénom")
    def full_name(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"

    @admin.display(description="livraison")
    def get_delivery(self):
        return f"{self.address}, {self.city}, {self.country}"
