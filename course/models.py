# course.models.py

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from course.managers import CourseManager, BookManager

from common.utilitary import img_url
from common.models import StatusAndPublishedMixin, BaseTimeStampModel, UUIDSlugMixin


NULL_AND_BLANK = {'null': True, 'blank': True}


class Course(UUIDSlugMixin, StatusAndPublishedMixin, BaseTimeStampModel):

    T = 'En Ligne'
    O = 'En Présentiel'

    OPTION_COURSE_CHOICES = (
        (T, 'En Ligne'),
        (O, 'En Présentiel')
    )
    file_prepend = "course/upload/"

    name = models.CharField(
        max_length=200,
        verbose_name="titre",
        help_text='Saisir le titre de cette formation (200 caractères maximum).'
    )
    subtitle = models.CharField(
        verbose_name='sous-titre',
        max_length=180,
        help_text='Saisir le sous-titre de cette formation (200 caractères maximum).',
        **NULL_AND_BLANK
    )
    price = models.PositiveIntegerField(
        default=5000,
        verbose_name='côut de la formation',
        validators=[
            MinValueValidator(5000),
            MaxValueValidator(1000000)
        ],
        help_text='Indiquer le côut de cette formation.'
    )
    date_of_course = models.DateTimeField(
        auto_now_add=False, auto_now=False,
        verbose_name='date & heure de la formation',
        help_text="Indiquer la date & l'heure de la formation"
    )
    location_of_course = models.CharField(
        max_length=200,
        verbose_name='Lieux de formation',
        help_text="Définir le lieux de la formation."
    )
    resume = models.TextField(
        max_length=300,
        verbose_name='résumé',
        help_text='faire un petit résumé de cette formation.',
        **NULL_AND_BLANK
    )
    description = models.TextField(
        verbose_name='description',
        help_text='décrire la formation, les rubriques et les objectifs.',
        **NULL_AND_BLANK
    )
    cover = models.ImageField(
        upload_to=img_url,
        verbose_name="ajouter une image",
        help_text="ajouter une image descriptive de l'article.",
        **NULL_AND_BLANK
    )
    view = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="nombre de vues"
    )
    option = models.CharField(
        default=O,
        max_length=13,
    	verbose_name="Option de la formation",
    	choices=OPTION_COURSE_CHOICES,
        help_text="Option de la formation"
    )

    objects = CourseManager()

    class Meta:
        ordering = ['-published']
        verbose_name_plural = 'formations'
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return self.name
    
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        while Course.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{get_random_string(6)}".lower()
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def course_absolute_url(self):
    	return reverse("course:course_detail", kwargs={"slug": str(self.slug)})


class Book(UUIDSlugMixin, StatusAndPublishedMixin, BaseTimeStampModel):

    file_prepend = "book/upload/"

    name = models.CharField(
        max_length=200,
        verbose_name="titre du livre",
        help_text='Saisir le titre du livre (200 caractères maximum).'
    )
    price = models.PositiveIntegerField(
        default=5000,
        verbose_name="prix de cet article",
        validators=[
            MinValueValidator(5000),
            MaxValueValidator(1000000)
        ],
        help_text='Indiquer le prix de cet article.'
    )
    resume = models.TextField(
        max_length=500,
        verbose_name='résumé du livre',
        help_text='faire un petit résumé de ce document (maximum 500 caractère)',
        **NULL_AND_BLANK
    )
    cover = models.ImageField(
        upload_to=img_url,
        verbose_name="ajouter une image de couverture",
        help_text="ajouter une image de couverture de ce livre.",
        **NULL_AND_BLANK
    )
    view = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="nombre de vues"
    )

    objects = BookManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'livres'
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return self.name
    
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        while Livre.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{get_random_string(6)}".lower()
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def book_absolute_url(self):
    	return reverse("book:book_detail", kwargs={"slug": str(self.slug)})
