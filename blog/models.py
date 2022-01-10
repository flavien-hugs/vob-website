# blog.models.py

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.core.validators import MaxValueValidator, MinValueValidator

from blog.managers import PostManager

from common.utilitary import img_url
from common.models import StatusAndPublishedMixin, BaseTimeStampModel, UUIDSlugMixin

import readtime
from taggit.managers import TaggableManager


NULL_AND_BLANK = {'null': True, 'blank': True}


class Category(UUIDSlugMixin, BaseTimeStampModel):

    M = 'Motivation'
    S = 'Spiritualité'
    E = 'Business & Entrepreneuriat'

    CATEGORIE_CHOICES = (
        (M, 'Motivation'),
        (S, 'Spiritualité'),
        (E, 'Business & Entrepreneuriat')
    )
    
    name = models.CharField(
        default=E,
        unique=True,
        max_length=30,
        choices=CATEGORIE_CHOICES,
        verbose_name="type de catégorie d'article",
        help_text="Définir le type de catégorie de l'article.",
        **NULL_AND_BLANK
    )

    class Meta:
        ordering = ['-name']
        verbose_name_plural = 'catégories'
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return self.name

    @admin.display(description="catégorie")
    def category_name(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{get_random_string(6)}".lower()
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def category_absolute_url(self):
        return reverse('blog:category_list', kwargs={"slug": self.slug})

    def posts(self):
        return Post.objects.filter(category=self)

    @admin.display(description="nombre d'articles dans cette catégorie")
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
        unique=True,
        max_length=255,
    	verbose_name="titre de l'article",
    	help_text="Définir le titre de l'article."
    )
    subtitle = models.CharField(
        max_length=255,
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
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000000)
        ],
        help_text='Si cet article est payant, indiquer le prix.'
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
        verbose_name="nombre de lecture"
    )
    reading = models.CharField(
        default=G,
        max_length=10,
    	choices=PAID_CHOICES,
    	verbose_name="Option de lecture",
        help_text="définir l'option de lecture de cet article."
    )

    tags = TaggableManager(verbose_name="mots clés")

    objects = PostManager()

    class Meta:
        ordering = ['-published']
        get_latest_by = ['-published']
        verbose_name_plural = 'articles'
        indexes = [models.Index(fields=['uuid'])]
    
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{get_random_string(6)}".lower()
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @admin.display(description="côut")
    def post_price(self):
        if self.price > 0:
            return f"{self.price} Fr/CFA"
        return "article gratuit"
    
    @admin.display(description="nombre de lecture")
    def post_count_viewed(self):
        return f"{self.view} lecture"
    
    @admin.display(description="temps de lecture")
    def readtime(self):
        readtime_post = readtime.of_text(self.body)
        return readtime_post

    @admin.display(description="mots clés")
    def tag_list(self):
        return u", ".join(o.name for o in self.tags.all())

    def post_absolute_url(self):
    	return reverse("blog:post_detail", kwargs={"slug": str(self.slug)})


@receiver([models.signals.pre_save], sender=Post)
def delete_old_cover(sender, instance, *args, **kwargs):
    if instance.pk:
        try:
            old_cover = Post.objects.get(pk=instance.pk).cover
            if old_cover and old_cover.url != instance.cover.url:
                old_cover.delete(save=False)
        except: pass
