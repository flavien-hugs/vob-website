# checkout.views.py

from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from course.models import Book

from checkout.models import Checkout
from checkout.forms import CheckoutForm
from common.utilitary import get_client_ip


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
                    'checkout:checkout_success_path',
                    kwargs={'id_checkout': checkout.id_checkout}
                )
            )
    else:
        form = CheckoutForm()

    context = {
        'form': form,
        'object': book,
        'page_title': book.name,
    }
    template = 'checkout/checkout_form.html'

    return render(request, template, context)


checkout_book_view = checkout_view


def checkout_success(request, id_checkout):

    id_checkout = request.session.get('id_checkout', 0)
    checkout = Checkout.objects.filter(id_checkout=id_checkout)

    context = {
        'object': checkout,
        'page_title': 'Commande validé avec succès',
    }
    template = 'checkout/checkout_success.html'
    return render(request, template, context)


checkout_success_view = checkout_success
