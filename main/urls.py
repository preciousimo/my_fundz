from django.urls import path
from main import views, transfer

urlpatterns = [
    path("", views.index, name="index"),

    # Transfers
    path("search-account/", transfer.search_users_account_number, name="search-account"),
]