# pages.views.py

from django.template import loader
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

from page.forms import ContactForm
from haystack.query import SearchQuerySet


def search(request):
    posts = SearchQuerySet().autocomplete(
        name=request.POST.get('search', '')
    )
    context = {'posts': posts}
    html_template = loader.get_template("search/search.html")
    return HttpResponse(html_template.render(context, request))


search_view = search


def contact_view(request):
    
    form = ContactForm()

    if request.method == "POST" and request.is_ajax() :
        form = ContactForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data['name']
            form.save()
            messages.add_message(
                request, messages.SUCCESS,
                "Merci ! Nous vous contacterons bientôt."
            )
            return JsonResponse({"name": name}, status=200)
        else:
            errors = form.errors.as_json()
            return JsonResponse({"errors": errors}, status=400)

    context = {
        'form': form,
        'page_title': "contactez-nous"
    }
    html_template = loader.get_template("flatpages/contact_page.html")
    return HttpResponse(html_template.render(context, request))


contact_view = contact_view
