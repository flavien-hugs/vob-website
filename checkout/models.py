# checkout.models.py

import uuid
import string
import random
import datetime
from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.contrib import admin
from django.utils.timezone import now
from course.models import Course, Book
from common.models import BaseTimeStampModel, UserBaseInfo

NULL_AND_BLANK = {'null': True, 'blank': True}


def random_checkout_code():
    order_code = "".join(random.choices(string.digits, k=8))
    return order_code


class ModelCheckoutRegisterMixin(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid'
    )

    ip_address = models.GenericIPAddressField(
        max_length=180,
        protocol='both',
        unpack_ipv4=False,
        verbose_name='adresse ip',
        **NULL_AND_BLANK
    )
    class Meta:
        abstract = True


class Checkout(ModelCheckoutRegisterMixin, UserBaseInfo, BaseTimeStampModel):

    id_checkout = models.CharField(
        max_length=8,
        verbose_name='N° Commande',
        editable=False, unique=True,
        default=random_checkout_code
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='livre',
    )
    date_added = models.DateTimeField(
        verbose_name="Date de la commande",
        db_index=True, default=now
    )

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = "commande de livre"
        indexes = [models.Index(fields=['uuid'])]

    def clean(self):
        if (
            self.date_added.date() <= self.date_of_course.date()
        ):
            raise ValidationError(
                {"date_added": "Cette formation est déjà passé !"}
            )

    def __str__(self):
        return f"Commande - {self.id_checkout}"

    @admin.display(description="prix")
    def get_book_cost(self):
        return f"{self.book.price} frcfa".upper()

    @admin.display(description="date de la commande")
    def get_order_book(self):
        return self.date_added.date()

    def get_absolute_url(self):
        return reverse(
            "checkout_book:checkout_path",
            kwargs={"slug": self.book.slug}
        )


class RegisterCourse(ModelCheckoutRegisterMixin, UserBaseInfo, BaseTimeStampModel):

    id_checkout = models.CharField(
        max_length=8,
        verbose_name='ID Inscription',
        editable=False, unique=True,
        default=random_checkout_code
    )
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name='course',
    )
    date_added = models.DateTimeField(
        verbose_name="Date d'Inscription",
        db_index=True, default=now
    )

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = "inscriptions"
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return f"Inscription - {self.id_checkout}"

    @admin.display(description="prix")
    def get_course_cost(self):
        return f"{self.course.price} frcfa".upper()

    @admin.display(description="date d'inscription")
    def get_signup_course(self):
        return self.date_added.date()

    def get_absolute_url(self):
        return reverse(
            "register_course:course_path",
            kwargs={"slug": self.book.slug}
        )
