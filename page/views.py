# pages.views.py

from django.template import loader
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

from page.forms import ContactForm
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet


def search(request):

    suggestions = SearchQuerySet().filter(
        name=AutoQuery(request.GET['search'])
    )
    context = {
        'items': suggestions,
        'count_items': suggestions.count()
    }
    html_template = loader.get_template("search/search.html")

    return HttpResponse(html_template.render(context, request))


search_view = search


def contact_view(request, template="flatpages/contact.html"):

    if request.method == "POST":
        form = ContactForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data['name']
            form.save()
            message = messages.success(
                request, f"Hello <strong>{name}</strong>, merci de m'avoir contacté.\
                <br> Je vous contacterais bientôt !"
            )
            data = {"name": name, "message": message}
            return JsonResponse(data, safe=False)
        else:
            messages.error(
                request, "Erreur !, veuillez vérifier les champs !"
            )
            messages.error(request, form.errors)
    else:
        form = ContactForm()

    context = {
        'form': form,
        'page_title': "contactez-moi"
    }
    
    return render(request, template, context)


contact_view = contact_view
