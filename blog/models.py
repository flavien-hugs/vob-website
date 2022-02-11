# blog.models.py

from itertools import chain

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver
from django.utils.text import Truncator
from django.core.validators import FileExtensionValidator

import readtime
from blog.managers import PostManager
from taggit.managers import TaggableManager

from common.utilitary import upload_image_to, unique_slug_generator
from common.models import StatusAndPublishedMixin, BaseTimeStampModel, UUIDSlugMixin


NULL_AND_BLANK = {'null': True, 'blank': True}


class Category(UUIDSlugMixin, BaseTimeStampModel):

    M = 'Motivation'
    S = 'Spiritualité'
    E = 'Business & Entrepreneuriat'

    file_prepend = "categorie/upload/"

    CATEGORIE_CHOICES = (
        (M, 'Motivation'),
        (S, 'Spiritualité'),
        (E, 'Business & Entrepreneuriat')
    )
    
    name = models.CharField(
        default=E,
        unique=True,
        max_length=180,
        choices=CATEGORIE_CHOICES,
        verbose_name="type de catégorie d'article",
        help_text="Définir le type de catégorie de l'article.",
    )
    cover = models.ImageField(
        upload_to=upload_image_to,
        verbose_name="ajouter une image",
        validators=[
            FileExtensionValidator(['jpeg', 'jpg', 'png'])
        ],
        help_text="ajouter une image descriptive de cette catégorie.",
        **NULL_AND_BLANK
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'catégories'
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return self.name
    
    def get_image_url(self):
        if self.cover:
            return self.cover.url
        return 'https://via.placeholder.com/300'

    @admin.display(description="catégorie")
    def category_name(self):
        return self.name

    def category_absolute_url(self):
        return reverse('categorie:category_list', kwargs={"slug": self.slug})

    def posts(self):
        return Post.objects.filter(category=self)

    @admin.display(description="nombre d'articles")
    def post_count(self):
        return self.posts().count()


class Post(UUIDSlugMixin, StatusAndPublishedMixin, BaseTimeStampModel):

    G = 'Gratuit'
    Y = 'Payant'

    PAID_CHOICES = (
        (G, 'Gratuit'),
        (Y, 'Payant')
    )
    
    file_prepend = "article/upload/"

    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        verbose_name="catégorie",
        **NULL_AND_BLANK
    )
    name = models.CharField(
        max_length=180,
    	verbose_name="titre de l'article",
    	help_text="Définir le titre de l'article."
    )
    subtitle = models.CharField(
        max_length=225,
    	verbose_name="sous-titre",
    	help_text="Définir un sous-titre de l'article.",
        **NULL_AND_BLANK
    )
    body = models.TextField(
        verbose_name="Contenu de l'article",
        help_text="Éditer le contenu de l'article."
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="prix de cet article",
        help_text='Si cet article est payant, indiquer le prix.',
        blank=True
    )
    cover = models.ImageField(
        upload_to=upload_image_to,
        verbose_name="ajouter une image",
        validators=[
            FileExtensionValidator(['jpeg', 'jpg', 'png'])
        ],
        help_text="ajouter une image descriptive de l'article.",
    )
    view = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="nombre de lecture"
    )
    reading = models.CharField(
        default=G,
        max_length=10,
    	choices=PAID_CHOICES,
    	verbose_name="Option de lecture",
        help_text="définir l'option de lecture de cet article."
    )

    objects = PostManager()

    class Meta:
        ordering = ['-published']
        get_latest_by = ['-published']
        verbose_name_plural = 'articles'
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return self.name
    
    def get_image_url(self):
        if self.cover:
            return self.cover.url
        return 'https://via.placeholder.com/300'

    @admin.display(description="côut")
    def post_price(self):
        if self.price > 0:
            return f"{self.price} frcfa".upper()
        return "article gratuit"
    
    @admin.display(description="nombre de lecture")
    def post_count_viewed(self):
        return f"{self.view} lecture"
    
    @admin.display(description="temps de lecture")
    def readtime(self):
        readtime_post = readtime.of_text(self.body)
        return readtime_post
    
    def post_name(self):
        truncated_name = Truncator(self.name)
        return truncated_name.words(10)
    
    def post_excerpt(self):
        truncated_subtitle = Truncator(self.subtitle)
        return truncated_subtitle.words(20)

    def post_absolute_url(self):
    	return reverse(
            "post:post_detail",
            kwargs={
                "category_slug": str(self.category.slug),
                "slug": str(self.slug)
            }
        )


@receiver([models.signals.pre_save], sender=Post)
@receiver([models.signals.pre_save], sender=Category)
def slug_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver([models.signals.pre_save], sender=Post)
@receiver([models.signals.pre_save], sender=Category)
def delete_old_cover(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            Klass = instance.__class__
            old_cover = Klass.objects.get(pk=instance.pk).cover
            if old_cover and old_cover.url != instance.cover.url:
                old_cover.delete(save=False)
        except: pass


