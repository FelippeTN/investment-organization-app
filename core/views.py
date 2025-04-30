from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Operation, Asset
from .forms import OperationForm
from django.db.models import Sum, F, Case, When, Value, IntegerField, DecimalField


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def welcome_page(request):
    return render(request, 'welcome.html')

@login_required
def home_page(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    # Fetch all global assets
    assets = Asset.objects.all()
    
    # Fetch operations for the current user
    operations = Operation.objects.filter(user=request.user).order_by('-date')
    
    # Compute portfolio: aggregate quantity and total value per asset for the user
    portfolio = {}
    portfolio_total = 0
    
    for asset in assets:
        # Calculate net quantity (compras - vendas) for the user
        qty = Operation.objects.filter(asset=asset, user=request.user).aggregate(
            net_quantity=Sum(
                Case(
                    When(type='compra', then=F('quantity')),
                    When(type='venda', then=-F('quantity')),
                    output_field=IntegerField()
                )
            )
        )['net_quantity'] or 0
        
        # Calculate total value (using latest unitary price for simplicity)
        latest_op = Operation.objects.filter(asset=asset, user=request.user).order_by('-date').first()
        total_value = qty * float(latest_op.unitary_price) if latest_op and qty > 0 else 0
        
        if qty > 0:  # Only include assets with positive quantity
            portfolio[asset.ticker] = {
                'quantity': qty,
                'total_value': total_value
            }
            portfolio_total += total_value
    
    return render(request, 'dashboard.html', {
        'operations': operations,
        'portfolio': portfolio,
        'portfolio_total': portfolio_total,
        'assets': assets
    })


@login_required
def operation_create(request):
    if request.method == 'POST':
        form = OperationForm(request.POST)
        if form.is_valid():
            operation = form.save(commit=False)
            operation.user = request.user
            operation.asset = form.cleaned_data['asset']
            operation.save()
            return redirect('dashboard')
    else:
        form = OperationForm()
    return render(request, 'operations/operation_form.html', {'form': form})