from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Account

# Create your forms here.


class NewUserForm(UserCreationForm):

    email = forms.EmailField()
    username = forms.CharField(max_length=20)
    firstname = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)
    country = forms.CharField(max_length=20)
    city = forms.CharField(max_length=30)
    street = forms.CharField(max_length=30)
    postcode = forms.CharField(max_length=10)

    class Meta:
        model = Account
        fields = '__all__'

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

