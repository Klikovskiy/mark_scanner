from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView
from django.views.generic import (TemplateView, RedirectView)

from scanner_auth.forms import LoginUserForm, SignUpForm
from scanner_auth.token_gen import token_generator

User = get_user_model()


class SignUp(CreateView):
    """
    Регистрация пользователя.
    """

    form_class = SignUpForm
    success_url = reverse_lazy('scanner_auth:check_email')
    template_name = 'auth/signup.html'

    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = form.save()
        user.is_active = False
        user.save()
        form.send_activation_email(self.request, user)
        return to_return


class ActivateEmail(RedirectView):
    """
    Активация почты нового пользователя.
    """

    url = reverse_lazy('scanner_auth:success')

    def get(self, request, uidb64, token):

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return super().get(request, uidb64, token)
        else:
            return render(request, 'auth/activate_account_invalid.html')


class CheckEmailView(TemplateView):
    """
    Сообщение, что бы пользователь проверил свою почту.
    """

    template_name = 'auth/check_email.html'


class SuccessView(TemplateView):
    """
    Успешная активация.
    """

    template_name = 'auth/success.html'


class LoginUser(LoginView):
    """
    Авторизация пользователя.
    """

    form_class = LoginUserForm
    template_name = 'auth/login.html'

    def get_success_url(self):
        return reverse_lazy('home')
