from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.forms.widgets import PasswordInput
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from scanner_auth.token_gen import token_generator

User = get_user_model()


class SignUpForm(UserCreationForm):
    """
    Форма регистрация нового пользователя в системе.
    """

    email = forms.CharField(
        label='Электронная почта',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form__input',
                                      'type': 'email'})
    )
    password1 = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form__input',
            'type': 'password'})
    )
    password2 = forms.CharField(
        label='Повтор пароля',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form__input',
            'type': 'password'})
    )

    user_public_contract = forms.BooleanField(
        label='Согласен с',
        required=True,
        widget=forms.CheckboxInput(
            attrs={'class': 'form__agree',
                   'type': 'checkbox'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2')

    def send_activation_email(self, request, user):
        current_site = get_current_site(request)
        subject = 'Активируйте вашу учетную запись'
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


class LoginUserForm(AuthenticationForm):
    """
    Форма входа пользователя.
    """

    redirect_authenticated_user = True

    password = forms.CharField(
        label='Пароль',
        widget=PasswordInput(attrs={'class': 'form__input',
                                    'type': 'password'})
    )

    username = forms.CharField(
        label='Электронная почта',
        widget=forms.TextInput(
            attrs={'class': 'form__input',
                   'type': 'email'}
        )
    )  # username - это почта, из-за переопределения стандартной модели.

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username,
                                           password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(email=username)
                except ObjectDoesNotExist:
                    user_temp = None
                if user_temp is not None:
                    raise forms.ValidationError('Эта учётная запись отключена '
                                                'администратором или Вы не '
                                                'подтвердили свою почту.')
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
        return self.cleaned_data

    field_order = ['username', 'password']
