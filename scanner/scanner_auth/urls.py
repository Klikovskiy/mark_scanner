from django.contrib.auth import views as auth_views
from django.urls import path

from scanner_auth.views import (LoginUser, SuccessView,
                                CheckEmailView, ActivateEmail, SignUp)

app_name = 'scanner_auth'

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateEmail.as_view(),
         name='activate'),
    path('check-email/', CheckEmailView.as_view(), name='check_email'),
    path('success/', SuccessView.as_view(), name='success'),
    path('login/',
         LoginUser.as_view(redirect_authenticated_user=True,
                                     template_name='auth/login.html'),
         name='login'),
    path('logout/',
         auth_views.LogoutView.as_view(template_name='auth/logout.html'),
         name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='auth/password/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='auth/password/password_sent.html'),
         name='password_reset_done', ),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='auth/password/password_confirm.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='auth/password/password_complete.html'),
         name='password_reset_complete'),
]
