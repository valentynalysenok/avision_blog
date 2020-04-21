from django import forms

from .models import ContactUs


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        exclude = ('created',)

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control mt-2', 'placeholder': 'Full Name', 'required': 'required'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-control mt-2', 'placeholder': 'Email', 'required': 'required'}),
            'body': forms.Textarea(attrs={
                'class': 'form-control mt-2', 'placeholder': 'Type your message here...'})
        }
