from django import forms
from .models import Subscriber
from django.forms import ModelForm


class NewsLetterSignUpForm(forms.ModelForm):
    #email = forms.CharField(label="Enter your email", max_length=100)
    class Meta:
        model = Subscriber
        fields = ['email']

        def clean_email(self):
            email = self.cleaned_data.get('email')
            return email