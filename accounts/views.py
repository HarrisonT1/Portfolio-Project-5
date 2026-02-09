from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserAccountForm
from .models import UserAccount
# Create your views here.


@login_required
def view_account(request):
    account, _ = UserAccount.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserAccountForm(instance=account)

    context = {
        'form': form,
    }

    return render(request, 'accounts/account.html', context)
