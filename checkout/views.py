# checkout.views.py

from django.urls import reverse
from django.views import generic
from django.shortcuts import render, redirect, get_object_or_404

from course.models import Course, Book

from common.utilitary import get_client_ip
from checkout.tasks import(
    send_email_for_checkout,
    send_email_for_register_course
)
from checkout.models import Checkout, RegisterCourse
from checkout.forms import CheckoutForm, CourseRegisterForm


def checkout_view(request, slug):

    book = get_object_or_404(Book, slug=slug)

    if request.method == "POST":
        data = request.POST.copy()
        form = CheckoutForm(data)

        if form.is_valid():

            checkout = Checkout()
            form = CheckoutForm(request.POST, instance=checkout)

            form.instance.book = book
            checkout = form.save(commit=False)

            checkout.book = book
            checkout.ip_address = get_client_ip(request)

            checkout.save()

            send_email_for_checkout.delay(checkout.pk)

            request.session['id_checkout'] = str(checkout.pk)
            return redirect(checkout.get_success_url())
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'object': book,
        'page_title': book.name,
        'breadcrumb_title': "Paiement"
    }
    template = 'checkout/_book_checkout_form.html'

    return render(request, template, context)


checkout_book_view = checkout_view


def course_register_view(request, slug):

    course = get_object_or_404(Course, slug=slug)

    if request.method == "POST":
        data = request.POST.copy()
        form = CourseRegisterForm(data)

        if form.is_valid():

            register = RegisterCourse()
            form = CourseRegisterForm(request.POST, instance=register)

            form.instance.course = course
            register = form.save(commit=False)

            register.course = course
            register.ip_address = get_client_ip(request)

            register.save()

            send_email_for_register_course.delay(register.pk)

            request.session['id_checkout'] = str(register.pk)
            return redirect(register.get_success_url())
    else:
        form = CourseRegisterForm()

    context = {
        'form': form,
        'object': course,
        'page_title': course.name,
        'breadcrumb_title': "Inscription",
    }
    template = 'checkout/checkout_base.html'

    return render(request, template, context)


course_register_view = course_register_view


def checkout_success(request, id_checkout):

    id_checkout = request.session.get('id_checkout')
    checkout = get_object_or_404(Checkout, pk=id_checkout)

    message = f"""
        Hello <strong>{checkout.full_name()}</strong>,<br> votre commande du livre <strong class="fs-italic">'{checkout.book.name}'</strong>.<br>
        Votre identifiant de commande est le <strong>{checkout.id_checkout}</strong>.<br>
        Veuillez le noté pour le retrait de votre livre.<br><br>

        Merci, Valère Obeï.
    """

    context = {
        'message': message,
        'page_title': 'Success',
    }
    template = 'checkout/checkout_success.html'
    return render(request, template, context)


checkout_success_view = checkout_success


def register_success(request, id_checkout):

    id_checkout = request.session.get('id_checkout')
    checkout = get_object_or_404(RegisterCourse, pk=id_checkout)

    message = f"""
        Hello {checkout.full_name()}, <br>
        merci pour votre intéret pour ce cours {checkout.course.name}.<br><br>
        Votre identifiant d'enregistrement est le <strong>{checkout.id_checkout}</strong>.<br>
        Veuillez le noté pour accéder au cours.<br><br>

        Merci, Valère Obeï.
    """

    context = {
        'message': message,
        'page_title': 'Success',
    }
    template = 'checkout/checkout_success.html'
    return render(request, template, context)


register_success_view = register_success
