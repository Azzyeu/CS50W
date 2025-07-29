from django.shortcuts import render, redirect
from django.urls import reverse

from . import util
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def load_page(request, title):
    markdowner = Markdown()
    try:
        html = markdowner.convert(util.get_entry(title))
    except:
        return render(request, "encyclopedia/page.html", {
            'title': "Page Not Found",
            'content': "<h1>Page Not Found</h1>"})

    return render(request, "encyclopedia/page.html", {
        'title': title,
        'content': html
    })

def search(request):
    query = request.GET["q"]
    
    for entry in util.list_entries():
        if query.lower() == entry.lower():
            return redirect(reverse("load_page", args=[query]))
    return render(request, "encyclopedia/search.html", {
        'query': query,
        'entries': util.list_entries()
    })