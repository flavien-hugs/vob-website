# course.models.py

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver
from django.utils.text import Truncator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from course.managers import CourseManager, BookManager

import tagulous.models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

from common.utilitary import upload_image_to, unique_slug_generator
from common.models import StatusAndPublishedMixin, BaseTimeStampModel, UUIDSlugMixin


NULL_AND_BLANK = {'null': True, 'blank': True}


class Course(UUIDSlugMixin, StatusAndPublishedMixin, BaseTimeStampModel):

    T = 'En Ligne'
    P = 'En Présentiel'

    OPTION_COURSE_CHOICES = (
        (T, 'En Ligne'),
        (P, 'En Présentiel')
    )
    file_prepend = "course/upload/"

    name = models.CharField(
        max_length=80,
        verbose_name="titre de la formation",
        help_text='Saisir le titre de cette formation (80 caractères maximum).'
    )
    subtitle = models.CharField(
        max_length=200,
        verbose_name='sous-titre',
        help_text='Saisir le sous-titre de cette formation (200 caractères maximum).',
        **NULL_AND_BLANK
    )
    price = models.PositiveIntegerField(
        default=5000,
        verbose_name='côut de la formation',
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
        help_text="Définir le lieux de la formation (200 caractères maximum)"
    )
    description = models.TextField(
        verbose_name='description',
        help_text='décrire la formation, les rubriques et les objectifs.',
    )
    cover = models.ImageField(
        upload_to=upload_image_to,
        verbose_name="ajouter une image",
        validators=[
            FileExtensionValidator(['jpeg', 'jpg', 'png'])
        ],
        help_text="ajouter une image descriptive de l'article.",
    )
    formatted_cover = ImageSpecField(
        source='cover',
        processors=[
            Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(923, 498)
        ],
        format='JPEG',
        options={'quality': 90}
    )
    view = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="nombre de vues"
    )
    option = models.CharField(
        default=P,
        max_length=13,
    	verbose_name="Option de la formation",
    	choices=OPTION_COURSE_CHOICES,
        help_text="Option de la formation"
    )
    tags = tagulous.models.TagField(
        verbose_name="mots clés",
        force_lowercase=True,
        max_count=2,
        blank=True,
        get_absolute_url=lambda tag: reverse(
            "course:course_tag_list",
            kwargs={'tag_slug': tag.slug}
        ),
    )
    objects = CourseManager()

    class Meta:
        ordering = ['-published']
        get_latest_by = ['-published']
        verbose_name_plural = 'formations'
        indexes = [models.Index(fields=['uuid'])]

    def clean(self):
        if (
            self.published <= self.date_of_course
        ):
            raise ValidationError(
                {
                    "published": "La date de publication ne doit pas \
                    être supérieure ou égale à la date de début de formation."
                }
            )

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.formatted_cover:
            return self.formatted_cover.url
        return 'https://via.placeholder.com/300'

    def course_name_excerpt(self):
        truncated_name = Truncator(self.name)
        return truncated_name.words(7)

    def course_subtitle_excerpt(self):
        truncated_subtitle = Truncator(self.subtitle)
        return truncated_subtitle.words(20)

    def course_excerpt(self):
        truncated_resume = Truncator(self.description)
        return truncated_resume.words(13)

    def course_tags(self):
        return self.tags.all()
    
    @admin.display(description="côut")
    def course_price(self):
        return f"{self.price} frcfa".upper()

    @admin.display(description="date")
    def course_date(self):
        return f"Le {self.date_of_course.date()} à {self.date_of_course.time()}"
    
    @admin.display(description="nombre de vues")
    def course_count_viewed(self):
        return f"{self.view} vues"

    def course_option(self):
        return self.get_option_display()

    def get_absolute_url(self):
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
        help_text='Indiquer le prix de cet article.'
    )
    resume = models.TextField(
        max_length=500,
        verbose_name='résumé du livre',
        help_text='faire un petit résumé de ce document (maximum 500 caractère)',
        **NULL_AND_BLANK
    )
    cover = models.ImageField(
        upload_to=upload_image_to,
        verbose_name="ajouter une image de couverture",
        validators=[
            FileExtensionValidator(['jpeg', 'jpg', 'png'])
        ],
        help_text="ajouter une image de couverture de ce livre.",
    )
    formatted_cover = ImageSpecField(
        source='cover',
        processors=[
            Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(923, 498)
        ],
        format='JPEG',
        options={'quality': 90}
    )
    view = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="nombre de vues"
    )

    objects = BookManager()

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = 'livres'
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.formatted_cover:
            return self.formatted_cover.url
        return 'https://via.placeholder.com/300'
    
    @admin.display(description="côut")
    def book_price(self):
        return f"{self.price} frcfa".upper()
    
    @admin.display(description="nombre de vues")
    def book_count_viewed(self):
        return f"{self.view} vues"

    def get_absolute_url(self):
    	return reverse("book:book_detail", kwargs={"slug": str(self.slug)})


@receiver([models.signals.pre_save], sender=Book)
@receiver([models.signals.pre_save], sender=Course)
def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver([models.signals.pre_save], sender=Book)
@receiver([models.signals.pre_save], sender=Course)
def delete_old_cover(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            Klass = instance.__class__
            old_cover = Klass.objects.get(pk=instance.pk).cover
            
            if old_cover and old_cover.url != instance.cover.url:
                old_cover.delete(save=False)

            if old_formatted_cover and old_formatted_cover.url != instance.formatted_cover.url:
                old_formatted_cover.delete(save=False)
        except: pass
