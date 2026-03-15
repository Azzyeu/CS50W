from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:title>/", views.view_listing, name="view_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category", views.list_categories, name="list_categories"),
    path("category/<str:category>/", views.category, name="category")
]
