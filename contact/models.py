from django.db import models


class ContactUs(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    body = models.TextField(blank=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"
        ordering = ('-created',)

    def __str__(self):
        return f"{self.name} {self.email}"
