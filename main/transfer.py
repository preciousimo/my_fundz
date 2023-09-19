from django.shortcuts import render, redirect
from userauth.models import Account
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from decimal import Decimal
from main.models import Transaction


@login_required
def search_users_account_number(request):
    # account = Account.objects.filter(account_status="active")
    account = Account.objects.all()
    query = request.POST.get("account_number")

    if query:
        account = account.filter(
            Q(account_number=query)|
            Q(account_id=query)
        ).distinct()

    context = {
        "account": account,
        "query": query,
    }
    return render(request, "transfer/search_user_by_account_number.html", context)

def AmountTransfer(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request, "Account does not exist.")
        return redirect("main:search-account")
    context = {
        "account": account,
    }
    return render(request, "transfer/amount_transfer.html", context)

def AmountTransferProcess(request, account_number):
    account = Account.objects.get(account_number=account_number) 
    sender = request.user 
    reciever = account.user

    sender_account = request.user.account
    reciever_account = account

    if request.method == "POST":
        amount = request.POST.get("amount-send")
        description = request.POST.get("description")

        print(amount)
        print(description)

        if sender_account.account_balance >= Decimal(amount):
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                reciever=reciever,
                sender=sender,
                sender_account=sender_account,
                reciever_account=reciever_account,
                status="processing",
                transaction_type="transfer"
            )
            new_transaction.save()
            
            # Get the id of the transaction that vas created nov
            transaction_id = new_transaction.transaction_id
            return redirect("main:transfer-confirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, "Insufficient Fund.")
            return redirect("main:amount-transfer", account.account_number)
    else:
        messages.warning(request, "Error Occured, Try again later.")
        return redirect("userauth:account")
    
def TransferConfirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transaction does not exist.")
        return redirect("userauth:account")
    context = {
        "account":account,
        "transaction":transaction
    }
    return render(request, "transfer/transfer_confirmation.html", context)


def TransferProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user 
    reciever = account.user

    sender_account = request.user.account 
    reciever_account = account

    completed = False

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        print(pin_number)

        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()

            # Remove the amount that i am sending from my account balance and update my account
            sender_account.account_balance -= transaction.amount
            sender_account.save()

            # Add the amount that vas removed from my account to the person that i am sending the money too
            account.account_balance += transaction.amount
            account.save()

            messages.success(request, "Transfer Successfull.")
            return redirect("main:transfer-completed", account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, "Incorrect Pin.")
            return redirect('main:transfer-confirmation', account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, "An error occured, Try again later.")
        return redirect('userauth:account')


def TransferCompleted(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, "Transfer does not exist.")
        return redirect("userauth:account")
    context = {
        "account":account,
        "transaction":transaction
    }
    return render(request, "transfer/transfer_completed.html", context)
