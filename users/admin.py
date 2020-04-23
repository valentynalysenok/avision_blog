from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'created')
    list_filter = ('created', 'updated')
    search_fields = ('username', 'email')
    ordering = ('created',)
    list_per_page = 20
