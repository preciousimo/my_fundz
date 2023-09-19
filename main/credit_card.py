from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import CreditCard
from userauth.models import Account
from decimal import Decimal

@login_required
def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credic_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    context = {
        "userauth":account,
        "credic_card":credic_card,
    }
    return render(request, "credit_card/card_detail.html", context)

@login_required
def fund_credit_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account
    
    if request.method == "POST":
        amount = request.POST.get("funding_amount")
        
        if Decimal(amount) <= account.account_balance:
            account.account_balance -= Decimal(amount)
            account.save()
            
            credit_card.amount += Decimal(amount)
            credit_card.save()
            
            messages.success(request, "Funding Successfull")
            return redirect("main:card-detail", credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Funds")
            return redirect("main:card-detail", credit_card.card_id)

@login_required
def withdraw_fund(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)

    if request.method == "POST":
        amount = request.POST.get("amount")
        print(amount)

        if credit_card.amount >= Decimal(amount) and credit_card.amount != 0.00:
            account.account_balance += Decimal(amount)
            account.save()

            credit_card.amount -= Decimal(amount)
            credit_card.save()

            messages.success(request, "Withdrawal Successfull")
            return redirect("main:card-detail", credit_card.card_id)
        elif credit_card.amount == 0.00:
            messages.warning(request, "Insufficient Funds")
            return redirect("main:card-detail", credit_card.card_id)
        else:
            messages.warning(request, "Insufficient Funds")
            return redirect("main:card-detail", credit_card.card_id)
        
@login_required
def delete_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    
    account = request.user.account
    
    if credit_card.amount > 0:
        account.account_balance += credit_card.amount
        account.save()
            
        credit_card.delete()
        messages.success(request, "Card Deleted Successfull")
        return redirect("userauth:dashboard")
    
    credit_card.delete()
    messages.success(request, "Card Deleted Successfull")
    return redirect("userauth:dashboard")