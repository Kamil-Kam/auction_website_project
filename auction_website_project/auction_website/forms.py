from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Account

# Create your forms here.


class NewUAccountForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = '__all__'



