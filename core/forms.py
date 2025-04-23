from django import forms
from .models import Asset, Operation


class AssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'type', 'ticker']


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['asset', 'date', 'type', 'quantity', 'unitary_price', 'brokerage']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['asset'].queryset = Asset.objects.filter(user=user)