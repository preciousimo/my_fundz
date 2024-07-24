from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.models import CreditCard
from userauth.models import Account
from decimal import Decimal

# Define a constant for the redirect URL
CARD_DETAIL_URL = "main:card-detail"

# Define a constant for the insufficient funds message
INSUFFICIENT_FUNDS_MESSAGE = "Insufficient Funds"

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
            return redirect(CARD_DETAIL_URL, credit_card.card_id)
        else:
            messages.warning(request, INSUFFICIENT_FUNDS_MESSAGE)
            return redirect(CARD_DETAIL_URL, credit_card.card_id)

@login_required
def withdraw_fund(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    if request.method == "POST":
        amount = Decimal(request.POST.get("amount"))
        
        # Define a small tolerance for floating point comparisons
        EPSILON = Decimal('0.00001')
        
        if credit_card.amount >= amount - EPSILON:
            account.account_balance += amount
            account.save()
            credit_card.amount -= amount
            credit_card.save()
            messages.success(request, "Withdrawal Successful")
            return redirect(CARD_DETAIL_URL, credit_card.card_id)
        else:
            messages.warning(request, INSUFFICIENT_FUNDS_MESSAGE)
            return redirect(CARD_DETAIL_URL, credit_card.card_id)
        
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