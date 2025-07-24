from django.shortcuts import render
from django.http import HttpResponse

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