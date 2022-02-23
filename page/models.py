# pages.models.py

import uuid

from django.db import models
from django.dispatch import receiver
from django.core.validators import RegexValidator, FileExtensionValidator

from common.models import BaseTimeStampModel
from common.utilitary import upload_image_to
from page.managers import PageQuerySetManager

NULL_AND_BLANK = {'null': True, 'blank': True}


class Contact(BaseTimeStampModel):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid'
    )
    name = models.CharField(
        verbose_name="nom & prénoms",
        max_length=180,
    )
    email = models.EmailField(
        verbose_name="email",
        max_length=180, null=True,
        help_text="votre adresse email"
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
        help_text="Entrer votre numéro de téléphone",
    )
    subject = models.CharField(
        max_length=180,
        verbose_name="sujet",
        help_text="sujet du message"
    )
    message = models.TextField(
        verbose_name='message',
        help_text="votre message"
    )

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = 'Contact'
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Testimonial(BaseTimeStampModel):

    file_prepend = "testimonial/upload/"

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid'
    )
    status = models.CharField(
        max_length=100,
        verbose_name="status",
        help_text='Entrer la prefession du client',
    )
    content = models.TextField(
        max_length=200,
        verbose_name="message",
        help_text='Entrer le message du client'
    )
    cover = models.ImageField(
        upload_to=upload_image_to,
        verbose_name="ajouter une image",
        validators=[
            FileExtensionValidator(['jpeg', 'jpg', 'png'])
        ],
        help_text="ajouter une photo de profile",
        **NULL_AND_BLANK
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="rendre visible ?",
        help_text='rendre visible cet témoignage ?'
    )

    objects = PageQuerySetManager()

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = 'Témoignages'
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return f"{self.name} - {self.status}"


@receiver([models.signals.pre_save], sender=Testimonial)
def delete_old_image(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            Klass = instance.__class__
            old_cover = Klass.objects.get(pk=instance.pk).cover
            if old_cover and old_cover.url != instance.cover.url:
                old_cover.delete(save=False)
        except:
            pass
