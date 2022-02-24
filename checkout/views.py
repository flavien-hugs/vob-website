# checkout.views.py

from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from course.models import Course, Book

from common.utilitary import get_client_ip
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

            return HttpResponseRedirect(
                reverse(
                    'checkout_book:checkout_success_path',
                    kwargs={'id_checkout': checkout.id_checkout}
                )
            )
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'object': book,
        'page_title': book.name,
        'breadcrumb_title': "Paiement"
    }
    template = 'checkout/form.html'

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

            return HttpResponseRedirect(
                reverse(
                    'checkout_book:checkout_success_path',
                    kwargs={'id_checkout': register.id_checkout}
                )
            )
    else:
        form = CourseRegisterForm()

    context = {
        'form': form,
        'object': course,
        'page_title': course.name,
        'breadcrumb_title': "Inscription",
    }
    template = 'checkout/form.html'

    return render(request, template, context)


course_register_view = course_register_view


def checkout_success(request, id_checkout):

    checkout_id = request.session.get('id_checkout', 0)
    checkout = Checkout.objects.filter(id_checkout=checkout_id).first()
    print(checkout)

    context = {
        'object': checkout,
        'page_title': 'Succès',
    }
    template = 'checkout/checkout_success.html'
    return render(request, template, context)


checkout_success_view = checkout_success
