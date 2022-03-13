# blog.models.py

import logging
from itertools import chain

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.dispatch import receiver
from django.utils.text import Truncator
from django.core.validators import(
    MaxLengthValidator, MinLengthValidator,
    FileExtensionValidator
)
from django.core.cache import cache

import readtime
from blog.managers import PostManager

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, Adjust

from common.utilitary import(
    upload_image_to, unique_slug_generator,
    cache_decorator)
from common.models import(
    StatusAndPublishedMixin, BaseTimeStampModel,
    UUIDSlugMixin)

logger = logging.getLogger(__name__)

NULL_AND_BLANK = {'null': True, 'blank': True}

name_validator = MaxLengthValidator(
    limit_value=180,
    message="Le titre de l'article doit être inférieur ou égal à 180 caractères !"
)

subtitle_validator = MaxLengthValidator(
    limit_value=225,
    message="Le titre de l'article doit être inférieur ou égal à 225 caractères !"
)


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
    formatted_cover = ImageSpecField(
        source='cover',
        processors=[
            Adjust(contrast=1.2, sharpness=1.1),
            ResizeToFill(120, 120)
        ],
        format='JPEG',
        options={'quality': 90}
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'catégories'
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return self.name

    def get_image_url(self):
        if self.formatted_cover:
            return self.formatted_cover.url
        return 'https://via.placeholder.com/300'

    @admin.display(description="catégorie")
    def category_name(self):
        return self.name.title()

    def get_absolute_url(self):
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
        validators=[name_validator],
    	verbose_name="titre de l'article",
    	help_text="Définir le titre de l'article."
    )
    subtitle = models.CharField(
        max_length=225,
    	verbose_name="sous-titre",
        validators=[name_validator],
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

    def save(self, *args, **kwargs):
        is_update_views = isinstance(
            self, Post
        ) and  'update_fields' in kwargs and kwargs['update_fields'] == ['view']

        if is_update_views:
            Post.objects.filter(pk=self.pk).update(view=self.view)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_admin_url(self):
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=(self.pk,))

    def get_image_url(self):
        if self.formatted_cover:
            return self.formatted_cover.url
        return 'https://via.placeholder.com/300'

    @admin.display(description="côut")
    def post_price(self):
        if self.price > 0:
            return f"{self.price} frcfa".upper()
        return "Gratuit"

    def viewed(self):
        self.view += 1
        self.save(update_fields=['view'])

    @admin.display(description="nombre de lecture")
    def post_count_viewed(self):
        return f"{self.view} lectures"

    @admin.display(description="temps de lecture")
    def readtime(self):
        readtime_post = readtime.of_text(self.body)
        return readtime_post

    def post_name(self):
        truncated_name = Truncator(self.name)
        return truncated_name.words(8)

    def post_excerpt(self):
        truncated_subtitle = Truncator(self.subtitle)
        return truncated_subtitle.words(20)

    def comments(self):
        return Comment.objects.filter(post=self)

    def comment_list(self):
        cache_key = f"post_comments_{self.pk}"
        value = cache.get(cache_key)
        if value:
            logger.info(f"get post comments:{self.pk}")
            return value
        else:
            post_comments = self.comments().filter(is_enable=True)
            cache.set(cache_key, post_comments, 60 * 100)
            logger.info(f"set post comments:{self.pk}")
            return post_comments

    @admin.display(description="nombre de commentaires")
    def comment_count(self):
        return self.comments().count()

    def get_absolute_url(self):
    	return reverse(
            "post:post_detail",
            kwargs={
                "category_slug": str(self.category.slug),
                "slug": str(self.slug)
            }
        )

    @cache_decorator(expiration=60 * 100)
    def next_post(self):
        return Post.objects.published().filter(pk__gt=self.pk).order_by('pk').first()

    @cache_decorator(expiration=60 * 100)
    def prev_post(self):
        return Post.objects.published().filter(pk__lt=self.pk).first()


class Comment(UUIDSlugMixin, BaseTimeStampModel):

    email = models.EmailField(
        max_length=80,
        verbose_name='adresse de messagerie'
    )
    name = models.CharField(
        verbose_name='nom & prénom',
        max_length=80
    )
    content = models.TextField(
        max_length=300,
        verbose_name='message'
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="article"
    )
    parent_comment = models.ForeignKey(
        to='self',
        on_delete=models.CASCADE,
        verbose_name="commentaire",
        **NULL_AND_BLANK
    )
    is_enable = models.BooleanField(
        default=True, verbose_name="active"
    )

    class Meta:
        ordering = ['-created_at']
        index_together = (('uuid'),)
        get_latest_by = ['-created_at']
        verbose_name_plural = 'commentaires'
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return f"{self.name} - {self.post.name}"

    def get_absolute_url(self):
        return reverse(
            'comment:comment_list',
            kwargs={'slug': str(self.post.slug)}
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

            if old_formatted_cover and old_formatted_cover.url != instance.formatted_cover.url:
                old_formatted_cover.delete(save=False)
        except: pass
