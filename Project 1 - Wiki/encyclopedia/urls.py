from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.load_page, name="load_page"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("random/", views.random, name="random")
]
