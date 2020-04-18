from time import time

from django.core.mail import EmailMessage
from django.utils.text import slugify


def custom_slugify(slug):
    new_slug = slugify(slug, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


def send_email(subject, message, email_to):
    email = EmailMessage(
        from_email='valentyna.lysenok@gmail.com',
        subject=subject,
        to=email_to,
        body=message
    )
    email.send()
