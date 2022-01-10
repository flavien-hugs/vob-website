# checkout.models.py

import uuid
import datetime

from django.db import models

from blog.models import Post
from course.models import Book
from common.models import BaseTimeStampModel, UserBaseInfo

NULL_AND_BLANK = {'null': True, 'blank': True}


def increment_order_number():
    year = str(datetime.date.today().year)
    month = str(datetime.date.today().month).zfill(2)
    last_order = Checkout.objects.order_by('uuid').last()
    if not last_order:
        return '' + year + month + '0000'
    
    order_number = last_order.order_number
    order_int = int(order_number[9:13])
    new_order_int = order_int + year + month + str(new_order_int).zfill(4)
    
    return new_order_id


class Checkout(UserBaseInfo, BaseTimeStampModel):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid'
    )
    id_checkout = models.CharField(
        max_length=500,
        verbose_name='ID Paiement',
        editable=False, unique=True,
        default=increment_order_number
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.SET_NULL,
        related_name='checkout_post',
        verbose_name='article',
        **NULL_AND_BLANK
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.SET_NULL,
        related_name='checkout_book',
        verbose_name='livre',
        **NULL_AND_BLANK
    )
    quantity = models.PositiveIntegerField(
        verbose_name='quantité',
        default=1
    )

    class Meta:
        ordering = ['-created_at']
        get_latest_by = ['-created_at']
        verbose_name_plural = "commande"
        indexes = [models.Index(fields=['uuid'])]

    def __str__(self):
        return f"{self.first_name} - {self.phone}- {self.id_checkout}"

    def get_post_cost(self):
        return self.post.price * self.quantity
    
    def get_book_cost(self):
        return self.book.price * self.quantity
