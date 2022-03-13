# checkout.forms.py

from django.utils.translation import gettext_lazy as _
from django import forms

from checkout.models import Checkout, RegisterCourse, Voucher


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Checkout
        exclude = [
            'book',
            'id_checkout',
            'ip_address',
            'created_at',
            'date_added'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control shadow-none'})
            if self.fields["payment"]:
                self.fields["payment"].widget.attrs.update({'class': 'form-select shadow-none'})

class CourseRegisterForm(forms.ModelForm):

    class Meta:
        model = RegisterCourse
        exclude = [
            'course',
            'address',
            'id_checkout',
            'ip_address',
            'created_at',
            'date_added',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control shadow-none'})


class VoucherForm(forms.Form):

    code = forms.CharField(
        label="Code promo",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'Entrer le code promo',
                'autocomplete': 'false'
            }))
