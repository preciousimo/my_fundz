from django.shortcuts import render, redirect
from main.models import Transaction
from userauth.models import Account
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def transaction_lists(request):
    sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by("-id")
    reciever_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="transfer").order_by("-id")

    request_sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request")
    request_reciever_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="request")

    context = {
        "sender_transaction":sender_transaction,
        "reciever_transaction":reciever_transaction,

        'request_sender_transaction':request_sender_transaction,
        'request_reciever_transaction':request_reciever_transaction,
    }

    return render(request, "transaction/transaction_list.html", context)

@login_required
def transaction_detail(request, transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    context = {
        "transaction":transaction,

    }

    return render(request, "transaction/transaction_detail.html", context)