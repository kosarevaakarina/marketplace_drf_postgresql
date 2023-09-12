from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from users.managers import UserManager


class UserRoles:
    SELLER = 'SELLER'
    CUSTOMER = 'CUSTOMER'

    ROLES = [
        (SELLER, 'SELLER'),
        (CUSTOMER, 'CUSTOMER')
    ]


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    first_name = models.CharField(max_length=50, verbose_name='имя пользователя')
    last_name = models.CharField(max_length=50, verbose_name='фамилия пользователя')
    phone = PhoneNumberField(unique=True, verbose_name='номер телефона')
    role = models.CharField(max_length=50, choices=UserRoles.ROLES, verbose_name='роль пользователя')

    is_active = models.BooleanField(default=True, verbose_name='активность пользователя')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.role})'

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save()
