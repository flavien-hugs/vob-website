# checkout.forms.py

from django import forms

from checkout.models import Checkout, RegisterCourse


class CheckoutForm(forms.ModelForm):

    class Meta:
        model = Checkout
        exclude = [
            'book',
            'id_checkout',
            'ip_address',
            'created_at',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control shadow-none'})


class CourseRegisterForm(forms.ModelForm):

    class Meta:
        model = RegisterCourse
        exclude = [
            'course',
            'address',
            'id_checkout',
            'ip_address',
            'created_at',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control shadow-none'})
