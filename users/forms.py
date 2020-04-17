from django import forms
from django_registration.forms import RegistrationFormUniqueEmail

from .models import CustomUser
from .utils import hunter, clearbit_signup


class CustomSignUpForm(RegistrationFormUniqueEmail):
    email = forms.EmailField(max_length=100, help_text='eg. youremail@mail.com')

    class Meta(RegistrationFormUniqueEmail.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        response = hunter.email_verifier(email)
        if response['result'] == 'undeliverable':
            raise forms.ValidationError('Email does not exist.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        user.first_name = clearbit_signup(user.email)[0]
        user.last_name = clearbit_signup(user.email)[1]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
