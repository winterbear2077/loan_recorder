import decimal

from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import User


# Create your views here.
def index(request):
    output_filed = DecimalField(max_length=12, decimal_places=4)
    user_with_totals = User.objects.annotate(
        total_lent=Coalesce(Sum('lender__debt_lender__principal'), 0, output_field=output_filed),
        total_borrowed=Coalesce(Sum('borrower__debt_borrower__principal'), 0, output_field=output_filed)
    )

    return render(request, 'loan_app/user.html', {'user_list': user_with_totals})


YEAR_SECONDS = 365 * 24 * 60 * 60


def calc_total(created_at, interest_rate: decimal.Decimal, principal: decimal.Decimal):
    elapsed_secs = (timezone.now() - created_at).total_seconds()
    result = principal * decimal.Decimal(elapsed_secs / YEAR_SECONDS) * interest_rate + principal
    return round(result, 4)


def detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    lent_debt = None
    borrow_debt = None
    if user.is_lender:
        lent_debt = user.lender.debt_lender.all()
        for debt in lent_debt:
            debt.total_amount = calc_total(debt.created_at, debt.interest_rate, debt.principal)

    if user.is_borrower:
        borrow_debt = user.borrower.debt_borrower.all()
        for debt in borrow_debt:
            debt.total_amount = calc_total(debt.created_at, debt.interest_rate, debt.principal)

    show_detail = {
        'username': user.name,
        'borrow_records': borrow_debt,
        'lent_records': lent_debt,
    }
    return render(request, 'loan_app/content.html', {'detail': show_detail})


def login(request):
    name = request.POST.get('username', 'Evan')
    user = get_object_or_404(User, name=name)
    user_id = user.get_id()
    return HttpResponseRedirect(reverse('loan_app:detail', args=(user_id,)))


def handle_404_default(request):
    return render(request, 'loan_app/404.html')