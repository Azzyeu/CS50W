from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

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

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)

def create(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            try:
                with open(f"entries/{title}.md") as f:
                    f.close()
                    return render(request, "encyclopedia/create.html", {
                        "flag": True
                    })
            except FileNotFoundError:
                with open(f"entries/{title}.md", "w") as f:
                    f.write(content)
    
            return redirect(reverse("load_page", args=[title]))
    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm()
    })

def edit(request, title):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            
            with open(f"entries/{title}.md", "w") as f:
                f.write(content)
            
            return redirect(reverse("load_page", args=[title]))
        
    return render(request, "encyclopedia/edit.html", {
        "form": NewPageForm(initial={
            "title": title,
            "content": util.get_entry(title)
        }),
        "title": title
    })
