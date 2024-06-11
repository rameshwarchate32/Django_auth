from django.forms import ModelForm

from .models import Customer


class customer_form(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
