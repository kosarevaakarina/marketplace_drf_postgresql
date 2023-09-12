from rest_framework.test import APITestCase

from market.models import Product
from users.models import User


class UserCreate(APITestCase):
    def setUp(self):
        self.percent = 1.06 * 1.02 * 1.20
        """Создание экземпляра товара пользователем-продавцом"""
        self.product = Product.objects.create(
            title='test',
            cost_price=1000,
            description='description'
        )
        self.product.price = self.product.cost_price * self.percent
        self.product.save()

    def create_user(self, role):
        """Создание и авторизация пользователя"""
        self.email = 'example@test.ru'
        user_data = {
            'email': self.email,
            'first_name': 'Test',
            'last_name': 'Testov',
            'phone': '+79999999999'
        }
        self.user = User(**user_data, role=role)
        self.user.set_password('123Qaz')
        self.user.save()
        response = self.client.post(
            '/users/token/',
            {
                'email': self.email,
                'password': '123Qaz'
            }
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def create_seller(self):
        """Создание пользователя-продавца"""
        self.create_user(role='SELLER')

    def create_customer(self):
        """Создание пользователя-покупателя"""
        self.create_user(role='CUSTOMER')

    def seller_binging(self):
        """Привязка авторизованного пользователя-продавца к товару"""
        self.create_seller()
        self.product.owner = self.user
        self.product.save()
        return self.product

    def customer_binging(self):
        """Привязка авторизованного пользователя-продавца к товару"""
        self.create_customer()
        self.product.owner = self.user
        self.product.save()
        return self.product
