from django.urls import path
from main import views, transfer

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),

    # Transfers
    path("search-account/", transfer.search_users_account_number, name="search-account"),
    path("amount-transfer/<account_number>/", transfer.AmountTransfer, name="amount-transfer"),
    path("amount-transfer-process/<account_number>/", transfer.AmountTransferProcess, name="amount-transfer-process"),
    path("transfer-confirmation/<account_number>/<transaction_id>/", transfer.TransferConfirmation, name="transfer-confirmation"),
    path("transfer-process/<account_number>/<transaction_id>/", transfer.TransferProcess, name="transfer-process"),
]