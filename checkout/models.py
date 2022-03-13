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
from django.core.validators import(
    RegexValidator, MinValueValidator,
    MaxValueValidator
)

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
    id_checkout = models.CharField(
        max_length=8,
        verbose_name='ID',
        editable=False, unique=True,
        default=random_checkout_code
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

    WAVE = "Wave"
    MTN = "MTN Money"
    MOOV = "Moov Money"
    ORANGE = "Orange Money"

    PAYMENT_CHOICES = (
        (WAVE, 'Wave'),
        (MTN, 'MTN Money'),
        (MOOV, 'Moov Money'),
        (ORANGE, 'Orange Money')
    )

    payment = models.CharField(
        default=WAVE,
        max_length=12,
    	choices=PAYMENT_CHOICES,
    	verbose_name="Moyen de paiement",
        help_text="Choisir le moyen de paiment."
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='books',
        verbose_name='livre',
    )
    transaction_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex='^\+?1?\d{9,15}$',
                message="Le numéro de téléphone de la transaction.",
                code='invalid_transaction_number'
            ),
        ],
        verbose_name='numéro de téléphone de la transaction',
        **NULL_AND_BLANK
    )
    transaction_code = models.CharField(
        unique=True, max_length=25,
        verbose_name="Identifiant du dépôt",
        help_text="référence de la transaction",
        **NULL_AND_BLANK
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
        unique_together = (('transaction_code', 'id_checkout'),)

    def __str__(self):
        return f"Commande - {self.id_checkout}"

    @admin.display(description="moyen de paiment")
    def get_payment_type(self):
        return self.get_payment_display()

    @admin.display(description="numéro de la transaction")
    def get_transaction_number(self):
        return int(self.transaction_number)

    @admin.display(description="ID de la transaction")
    def get_transaction_code(self):
        return int(self.transaction_code)

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

    def get_success_url(self):
        return reverse(
            "checkout_book:checkout_success_path",
            kwargs={"id_checkout": str(self.id_checkout)}
        )

    
class RegisterCourse(ModelCheckoutRegisterMixin, UserBaseInfo, BaseTimeStampModel):

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

    def get_success_url(self):
        return reverse(
            "register_course:register_success_path",
            kwargs={"id_checkout": str(self.id_checkout)}
        )

    def clean__date_added(self):
        if (
            self.date_added.date() <= self.course.date_of_course
        ):
            raise ValidationError(
                {"date_added": "Cette formation est déjà passé !"}
            )


class Voucher(BaseTimeStampModel):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid'
    )
    code = models.CharField(
        verbose_name="code",
        max_length=50, unique=True
    )
    valid_from = models.DateTimeField(
        verbose_name="Valable à partir de",
        default=datetime.datetime.now
    )
    valid_to = models.DateTimeField(
        verbose_name="Valable jusqu'à",
        default=datetime.datetime.now
    )
    discount = models.IntegerField(
        verbose_name="remise",
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    active = models.BooleanField(
        verbose_name="active",
        default=False
    )

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = "Coupons"
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return self.code
