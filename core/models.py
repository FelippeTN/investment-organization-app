from django.db import models

class Asset(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # Ação, FII, etc.
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return self.ticker

class Operation(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=10, choices=[('compra', 'Compra'), ('venda', 'Venda')])
    quantity = models.IntegerField()
    unitary_price = models.DecimalField(max_digits=10, decimal_places=2)
    brokerage = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.type} {self.asset.ticker}"