# course.models.py

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver
from django.utils.timezone import now
from django.utils.text import Truncator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

from course.managers import CourseManager, BookManager

import tagulous.models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

from common.utilitary import upload_image_to, unique_slug_generator
from common.models import(
    StatusAndPublishedMixin, BaseTimeStampModel,
    UUIDSlugMixin, VideoDescription
)


NULL_AND_BLANK = {'null': True, 'blank': True}


class Course(
    UUIDSlugMixin, StatusAndPublishedMixin,
    VideoDescription, BaseTimeStampModel
):

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
        help_text='Indiquer le côut de cette formation.',
        error_messages={
            "name": {
                "max_length": "The price must be between 0 and 999999",
            },
        },
    )
    discount_percentage = models.IntegerField(
        default=0,
        verbose_name="pourcentage de remise",
        **NULL_AND_BLANK
    )
    date_of_course = models.DateField(
        default=now,
        auto_now_add=False, auto_now=False,
        verbose_name='date & heure de la formation',
        help_text="Indiquer la date & l'heure de la formation"
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
    formatted_cover_featured = ImageSpecField(
        source='cover',
        processors=[
            Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(1140, 350)
        ],
        format='JPEG',
        options={'quality': 90}
    )
    option = models.CharField(
        default=P,
        max_length=13,
    	verbose_name="Type de la formation",
    	choices=OPTION_COURSE_CHOICES,
        help_text="Comment la formation se déroulera ? (En Présentiel ou En Ligne)"
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
    is_certificate = models.BooleanField(
        default=False,
        verbose_name="Certificat",
        help_text="Certificat de formation inclus après la formation",

    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Mettre en vedette",
        help_text="Mettre en vedette"
    )
    view = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="nombre de vues"
    )

    objects = CourseManager()

    class Meta:
        ordering = ['-published']
        get_latest_by = ['-published']
        verbose_name_plural = 'formations'
        indexes = [models.Index(fields=['uuid'])]

    def save(self, *args, **kwargs):
        is_update_views = isinstance(
            self, Course
        ) and 'update_fields' in kwargs and kwargs['update_fields'] == ['view']

        if is_update_views:
            Course.objects.filter(pk=self.pk).update(view=self.view)
        super().save(*args, **kwargs)

    def viewed(self):
        self.view += 1
        self.save(update_fields=['view'])

    def clean(self):
        if (
            self.published.date() <= self.date_of_course
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

    def name_excerpt(self):
        truncated_name = Truncator(self.name)
        return truncated_name.words(7)

    def course_subtitle_excerpt(self):
        truncated_subtitle = Truncator(self.subtitle)
        return truncated_subtitle.words(20)

    def resume_excerpt(self):
        truncated_resume = Truncator(self.description)
        return truncated_resume.words(13)

    def course_tags(self):
        return self.tags.all()

    def related_courses(self):
        return Course.objects.filter(
            tags__in=self.course_tags()
        ).exclude(pk=self.pk)

    @admin.display(description="côut")
    def course_price(self):
        return f"{int(self.price)} frcfa".upper()

    def discount_price(self):
        if self.discount_percentage > 0:
            price = self.price - ((self.price * self.discount_percentage) / 100)
            return round(price, 2)

    discount_price = property(discount_price)

    @admin.display(description="début de la formation")
    def course_date(self):
        return f"Le {self.date_of_course.strftime('%d %B %Y')}"

    @admin.display(description="nombre de vues")
    def count_viewed(self):
        return f"{self.viewed()} vues"

    def course_option(self):
        return self.get_option_display()

    def get_absolute_url(self):
    	return reverse("courses:course_detail", kwargs={"slug": str(self.slug)})

    def get_course_register_url(self):
    	return reverse(
            "register_course:register_course_path",
            kwargs={"slug": self.slug}
        )


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
        verbose_name='résumé du livre',
        help_text='faire un petit résumé de ce livre',
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
            ResizeToFill(923, 500)
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

    def save(self, *args, **kwargs):
        is_update_views = isinstance(
            self, Book
        ) and 'update_fields' in kwargs and kwargs['update_fields'] == ['view']

        if is_update_views:
            Book.objects.filter(pk=self.pk).update(view=self.view)
        super().save(*args, **kwargs)

    def viewed(self):
        self.view += 1
        self.save(update_fields=['view'])

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.formatted_cover:
            return self.formatted_cover.url
        return 'https://via.placeholder.com/300'

    def name_excerpt(self):
        truncated_name = Truncator(self.name)
        return truncated_name.words(7)

    def resume_excerpt(self):
        truncated_name = Truncator(self.resume)
        return truncated_name.words(13)

    @admin.display(description="côut")
    def book_price(self):
        return f"{self.price} frcfa".upper()

    @admin.display(description="nombre de vues")
    def count_viewed(self):
        return f"{self.view} vues"

    def recommended_books(self):
        from checkout.models import Checkout
        checkout = Checkout.objects.all()
        books = Book.objects.filter(books__in=checkout)
        return books

    def get_absolute_url(self):
    	return reverse(
            "book:book_detail",
            kwargs={"slug": str(self.slug)}
        )

    def get_checkout_url(self):
    	return reverse(
            "checkout_book:checkout_path",
            kwargs={"slug": self.slug}
        )


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
