from django import forms
from .models import Operation, Asset


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
        fields = ['asset', 'date', 'type', 'quantity', 'unitary_price', 'brokerage']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'bg-gray-700 text-white border border-gray-600 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-400'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'bg-gray-700 text-white border border-gray-600 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-400',
            })
            
        self.fields['asset'].queryset = Asset.objects.all()