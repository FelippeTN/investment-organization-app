from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=50, blank=True, null=True)  # Ex.: Ação, FII
    sector = models.CharField(max_length=100, blank=True, null=True)  # Sector from brapi
    current_price = models.FloatField(default=0.0)
    pl = models.FloatField(blank=True, null=True)  # P/L
    pvp = models.FloatField(blank=True, null=True)  # P/VP
    dividend_yield = models.FloatField(blank=True, null=True)  # Dividend Yield (%)

    def __str__(self):
        return f'{self.name} ({self.ticker})'

class Operation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=10, choices=[('compra', 'Compra'), ('venda', 'Venda')])
    quantity = models.IntegerField()
    unitary_price = models.DecimalField(max_digits=10, decimal_places=2)
    brokerage = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.type} {self.asset.ticker}"