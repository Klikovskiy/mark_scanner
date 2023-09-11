from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from scanner_auth.token_gen import token_generator


def send_activation_email(self, request, user):
    current_site = get_current_site(request)
    subject = 'Activate your Company account!'
    message = render_to_string(
        'emails/reg_user/user_activate_account.html',
        {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user),
        }
    )

    user.email_user(subject, message, html_message=message)
