from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import ContactUs
from .forms import ContactUsForm


class ContactUsView(SuccessMessageMixin, CreateView):
    model = ContactUs
    form_class = ContactUsForm
    template_name = 'contact.html'
    success_url = reverse_lazy('posts:posts_list')
    success_message = ""

    def form_valid(self, form):
        if form.is_valid():
            self.success_message = 'Your contact form sent successfully.'
        else:
            self.success_message = 'Your contact form wasn\'t sent.'
        return super().form_valid(form)
