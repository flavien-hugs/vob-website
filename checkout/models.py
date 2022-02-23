# checkout.models.py

import uuid
import string
import random
import datetime
from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.contrib import admin
from blog.models import Post
from course.models import Book
from common.models import BaseTimeStampModel, UserBaseInfo

NULL_AND_BLANK = {'null': True, 'blank': True}


def random_order_code():
    order_code = "".join(random.choices(string.digits, k=8))
    return order_code


class Checkout(UserBaseInfo, BaseTimeStampModel):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid'
    )
    id_checkout = models.CharField(
        max_length=8,
        verbose_name='ID Commande',
        editable=False, unique=True,
        default=random_order_code
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='livre',
    )
    ip_address = models.GenericIPAddressField(
        max_length=180,
        protocol='both',
        unpack_ipv4=False,
        verbose_name='adresse ip',
        **NULL_AND_BLANK
    )

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = "commande de livre"
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return f"Commande - {self.id_checkout}"

    @admin.display(description="prix")
    def get_book_cost(self):
        return f"{self.book.price} frcfa".upper()

    def get_absolute_url(self):
        return reverse(
            "checkout:checkout_path",
            kwargs={"slug": self.book.slug}
        )
