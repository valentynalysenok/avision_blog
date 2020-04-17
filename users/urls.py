from django.urls import path
from django_registration.backends.one_step.views import RegistrationView

from .forms import CustomSignUpForm

urlpatterns = [
    path('accounts/signup/', RegistrationView.as_view(
        form_class=CustomSignUpForm,
        success_url='/'
    ), name='django_registration_register'),

]
