from django.shortcuts import render, redirect
from userauth.models import KYC, Account
from userauth.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from main.forms import CreditCardForm
from main.models import CreditCard, Transaction


def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("userauth:kyc-reg")
        
        account = Account.objects.get(user=request.user)
    else:
        messages.warning(request, "You need to login to access the dashoard")
        return redirect("signin")

    context = {
        "kyc":kyc,
        "account":account,
    }
    return render(request, "userauth/account.html", context)

@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None
    
    if request.method == "POST":
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, "KYC Form submitted successfully, In review now.")
            return redirect("userauth:account")
    else:
        form = KYCForm(instance=kyc)
    context = {
        "account": account,
        "form": form,
        "kyc": kyc,
    }
    return render(request, "userauth/kyc_form.html", context)

def dashboard(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, "You need to submit your kyc")
            return redirect("userauth:kyc-reg")
        
        recent_transfer = Transaction.objects.filter(sender=request.user, transaction_type="transfer", status="completed").order_by("-id")[:1]
        recent_recieved_transfer = Transaction.objects.filter(reciever=request.user, transaction_type="transfer").order_by("-id")[:1]


        sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by("-id")
        reciever_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="transfer").order_by("-id")

        request_sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request")
        request_reciever_transaction = Transaction.objects.filter(reciever=request.user, transaction_type="request")
        
        
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by("-id")

        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user 
                new_form.save()
                
                card_id = new_form.card_id
                messages.success(request, "Card Added Successfully.")
                return redirect("userauth:dashboard")
        else:
            form = CreditCardForm()

    else:
        messages.warning(request, "You need to login to access the dashboard")
        return redirect("accounts:sign-in")

    context = {
        "kyc":kyc,
        "account":account,
        "form":form,
        "credit_card":credit_card,
        "sender_transaction":sender_transaction,
        "reciever_transaction":reciever_transaction,

        'request_sender_transaction':request_sender_transaction,
        'request_reciever_transaction':request_reciever_transaction,
        'recent_transfer':recent_transfer,
        'recent_recieved_transfer':recent_recieved_transfer,
    }
    return render(request, "userauth/dashboard.html", context)
    
    
@login_required
def change_pin(request):
    if request.method == "POST":
        current_pin = request.POST.get('current_pin')
        new_pin = request.POST.get('new_pin')
        confirm_new_pin = request.POST.get('confirm_new_pin')

        account = Account.objects.get(user=request.user)

        if current_pin != account.pin_number:
            messages.warning(request, "Invalid current PIN")
            return redirect("userauth:account")

        if new_pin != confirm_new_pin:
            messages.warning(request, "New PIN and Confirm New PIN do not match")
            return redirect("userauth:account")

        account.pin_number = new_pin
        account.save()

        messages.success(request, "PIN updated successfully")
        return redirect("userauth:dashboard")
    else:
        pass