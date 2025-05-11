from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Operation, Asset
from .forms import OperationForm
from django.db.models import Sum, F, Case, When, Value, IntegerField, DecimalField
from django.urls import reverse
import json 


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
    if request.user.is_authenticated:
        return redirect(reverse(home_page))
    return render(request, 'welcome.html')

@login_required
def home_page(request):
    return render(request, 'home.html')

@login_required
def dashboard(request):
    assets = Asset.objects.all()
    
    operations = Operation.objects.filter(user=request.user).order_by('-date')
    
    portfolio = {}
    portfolio_total = 0
    sector_totals = {}  
    
    for asset in assets:
        qty = Operation.objects.filter(asset=asset, user=request.user).aggregate(
            net_quantity=Sum(
                Case(
                    When(type='compra', then=F('quantity')),
                    When(type='venda', then=-F('quantity')),
                    output_field=IntegerField()
                )
            )
        )['net_quantity'] or 0
        
        total_cost = 0
        if qty > 0:
            operations_for_asset = Operation.objects.filter(asset=asset, user=request.user)
            for op in operations_for_asset:
                quantity = float(op.quantity)
                unitary_price = float(op.unitary_price)
                if op.type.lower() == 'compra':
                    total_cost += quantity * unitary_price
                elif op.type.lower() == 'venda':
                    total_cost -= quantity * unitary_price
        
        total_value = (total_cost / qty) * qty if qty > 0 else 0
        
        current_price = float(asset.current_price) if asset.current_price else 0
        
        if qty > 0: 
            portfolio[asset.ticker] = {
                'quantity': qty,
                'total_value': total_value, 
                'current_price': current_price,
                'sector': asset.sector or 'Desconhecido'  
            }
            portfolio_total += qty * current_price
            sector = asset.sector or 'Desconhecido'
            if sector not in sector_totals:
                sector_totals[sector] = 0
            sector_totals[sector] += qty * current_price
    
    sector_totals_json = json.dumps(sector_totals)
    
    return render(request, 'dashboard.html', {
        'operations': operations,
        'portfolio': portfolio,
        'portfolio_total': portfolio_total,
        'assets': assets,
        'sector_totals': sector_totals,
        'sector_totals_json': sector_totals_json  
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