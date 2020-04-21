from django.contrib import admin
from .models import ContactUs


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'body', 'created')
    list_filter = ('created',)
    search_fields = ('name', 'email')
    list_per_page = 20
