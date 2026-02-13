from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserAccountForm
from .models import UserAccount
from checkout.models import Order
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

    orders = account.orders.all().order_by('-date_time')

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    try:
        orders = paginator.page(page_number)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    context = {
        'form': form,
        'orders': orders
    }

    return render(request, 'accounts/account.html', context)


@login_required
def order_detail(request, order_number):
    order = get_object_or_404(
        Order,
        order_number=order_number,
        user=request.user.useraccount
    )

    regular_items = order.lineitems.filter(product__isnull=False).exists
    pick_and_mix_items = order.lineitems.filter(pick_and_mix_bag__isnull=False).exists

    context = {
        'regular_items': regular_items,
        'pick_and_mix_items': pick_and_mix_items,
        'order': order,
    }

    return render(request, 'accounts/order_detail.html', context)
