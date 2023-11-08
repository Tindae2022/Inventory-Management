from django import forms
from inventory.models import Sale, Customer, Product, Analytics


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'


class EmailForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    recipient = forms.EmailField()

