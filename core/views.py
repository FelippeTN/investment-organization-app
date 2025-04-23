from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Operation, Asset
from .forms import AssetForm, OperationForm
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


@login_required
def dashboard(request):
    # Fetch user's assets
    assets = Asset.objects.filter(user=request.user)
    
    # Fetch operations for user's assets
    operations = Operation.objects.filter(asset__user=request.user).order_by('-date')
    
    # Compute portfolio: aggregate quantity and total value per asset
    portfolio = {}
    for asset in assets:
        # Calculate net quantity (compras - vendas)
        qty = Operation.objects.filter(asset=asset).aggregate(
            net_quantity=Sum(
                Case(
                    When(type='compra', then=F('quantity')),
                    When(type='venda', then=-F('quantity')),
                    output_field=IntegerField()
                )
            )
        )['net_quantity'] or 0
        
        # Calculate total value (using latest unitary price for simplicity)
        latest_op = Operation.objects.filter(asset=asset).order_by('-date').first()
        total_value = qty * float(latest_op.unitary_price) if latest_op and qty > 0 else 0
        
        if qty > 0:  # Only include assets with positive quantity
            portfolio[asset.ticker] = {
                'quantity': qty,
                'total_value': total_value
            }
    
    return render(request, 'dashboard.html', {
        'operations': operations,
        'portfolio': portfolio,
        'assets': assets
    })


@login_required
def asset_list(request):
    assets = Asset.objects.filter(user=request.user).order_by('name')
    return render(request, 'assets/asset_list.html', {'assets': assets})


@login_required
def asset_create(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user
            asset.save()
            return redirect('dashboard')  # Redirect to dashboard instead
    else:
        form = AssetForm()
    return render(request, 'assets/asset_form.html', {'form': form})


@login_required
def asset_delete(request, pk):
    asset = Asset.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        asset.delete()
        return redirect('dashboard')
    return render(request, 'assets/asset_confirm_delete.html', {'asset': asset})


@login_required
def operation_create(request):
    if request.method == 'POST':
        form = OperationForm(request.POST, user=request.user)
        if form.is_valid():
            operation = form.save(commit=False)
            operation.asset = form.cleaned_data['asset']
            operation.save()
            return redirect('dashboard')
    else:
        form = OperationForm(user=request.user)
    return render(request, 'operations/operation_form.html', {'form': form})