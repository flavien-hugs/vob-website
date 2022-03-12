# checkout.tasks.py

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail

from checkout.models import Checkout, RegisterCourse


@shared_task
def send_email_for_checkout(id_checkout):

    """
        Task to send an email notification
        when an order is successfully created.
    """

    checkout = Checkout.objects.get(pk=id_checkout)
    subject = f"Commande N°{checkout.id_checkout}"
    message = f"""
        Bonjour {checkout.full_name()}, \n\nVotre commande a été validé avec success.
        L'identifiant de la commande est {checkout.id_checkout}.
    """

    send = send_mail(
        subject, message, settings.EMAIL_HOST_USER,
        [checkout.email], fail_silently=False,
    )

    return send


@shared_task
def send_email_for_register_course(id_checkout):
    """
        Task to send an email notification
        when an order is successfully created.
    """

    register = RegisterCourse.objects.get(pk=id_checkout)
    subject = f"ID {register.id_checkout} Register"
    message = f"""
        Bonjour {register.full_name()}, \n\nVotre Identifiant a été validé avec success.
        L'identifiant de la commande est {register.id_checkout}.
    """

    send = send_mail(
        subject, message, settings.EMAIL_HOST_USER,
        [register.email], fail_silently=False,
    )

    return send
