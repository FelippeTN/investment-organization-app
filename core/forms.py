from django import forms
from .models import Operation, Asset


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['asset', 'date', 'type', 'quantity', 'unitary_price', 'brokerage']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset'].queryset = Asset.objects.all()