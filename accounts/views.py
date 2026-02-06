from django.shortcuts import render

# Create your views here.


def view_account(request):
    return render(request, 'accounts/account.html')
