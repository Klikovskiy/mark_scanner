from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from scanner_user.validators import validate_email_domain


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('E-Mail is Required, Please Provide Your E-Mail.')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password
        )
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    """
    Дополнительные поля для пользователей.
    """

    is_active = models.BooleanField(
        default=False,
        verbose_name='Активация аккаунта',
        null=False,
    )

    username = models.CharField(
        default='-',
        max_length=150,
        verbose_name='Имя пользователя',
        unique=False,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        max_length=254,
        null=False,
        blank=False,
        unique=True,
        validators=[validate_email_domain]
    )

    price_multiply = models.IntegerField(
        verbose_name='Множитель цены',
        default=1,
        null=True,
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
