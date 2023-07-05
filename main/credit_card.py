from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import CreditCard
from account.models import Account

@login_required
def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credic_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    context = {
        "account":account,
        "credic_card":credic_card,
    }
    return render(request, "credit_card/card_detail.html", context)

