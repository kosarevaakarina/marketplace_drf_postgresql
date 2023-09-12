from rest_framework import status
from rest_framework.test import APITestCase
from market.tests.services import UserCreate


class UserRegisterAPITestCase(APITestCase):
    """Тестирование регистрации пользователя"""

    def test_register_user(self):
        response = self.client.post('/users/register/', {
            "email": "test@yandex.ru",
            "first_name": "First",
            "last_name": "Last",
            "phone": "+79999999999",
            "role": "SELLER",
            "password": "485967",
            "password2": "485967"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_user_with_fatal_phone(self):
        """Тестирование создания пользователя при неверно введенном номере телефона"""
        response = self.client.post('/users/register/', {
            "email": "test@yandex.ru",
            "first_name": "First",
            "last_name": "Last",
            "phone": "12345",
            "role": "SELLER",
            "password": "485967",
            "password2": "485967"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'phone': ['Введен некорректный номер телефона.']})

    def test_register_user_with_fatal_first_name(self):
        """Тестирование создания пользователя при неверно введенном имени пользователя"""
        response = self.client.post('/users/register/', {
            "email": "test@yandex.ru",
            "first_name": "First1",
            "last_name": "Last",
            "phone": "+79999999999",
            "role": "SELLER",
            "password": "485967",
            "password2": "485967"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Имя введено некорректно.']})

    def test_register_user_with_fatal_last_name(self):
        """Тестирование создания пользователя при неверно введенной фамилии пользователя"""
        response = self.client.post('/users/register/', {
            "email": "test@yandex.ru",
            "first_name": "First",
            "last_name": "Last1",
            "phone": "+79999999999",
            "role": "SELLER",
            "password": "485967",
            "password2": "485967"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Фамилия введена некорректно.']})


class UserListAPITestCase(UserCreate):
    """Тестирование просмотра пользователей"""

    def test_get_unauth_user(self):
        """Тестирование просмотра пользователей для неавторизованного пользователя"""
        response = self.client.get('/users/', )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_get_user(self):
        """Тестирование просмотра пользователей для авторизованного пользователя"""
        self.create_seller()
        response = self.client.get('/users/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{
            'email': 'example@test.ru',
            'first_name': 'Test',
            'last_name': 'Testov',
            'phone': '+79999999999',
            'role': 'SELLER'
        }])


class UserRetrieveAPITest(UserCreate):
    """Тестирование просмотра одного пользователя"""

    def retrieve_user(self, user_id):
        return self.client.get(f'/users/{user_id}/', )

    def test_retrieve_user(self):
        """Тестирование просмотра аккаунта пользователя"""
        self.create_seller()
        response = self.retrieve_user(self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'email': 'example@test.ru',
            'first_name': 'Test',
            'last_name': 'Testov',
            'phone': '+79999999999',
            'role': 'SELLER'})


class UserUpdateTestCase(UserCreate):
    """Тестирование обновления данных о пользователе"""

    def test_update_user(self):
        """Тестирование обновления пользователя"""
        self.create_seller()
        response = self.client.patch(f'/users/update/{self.user.pk}/', {'email': 'newtest@example.ru'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'email': 'newtest@example.ru',
            'first_name': 'Test',
            'last_name': 'Testov',
            'phone': '+79999999999',
            'role': 'SELLER'
        })

    def test_update_user_fatal_phone(self):
        """Тестирование обновления данных пользователя при неверно введенном номере телефона"""
        self.create_seller()
        response = self.client.patch(f'/users/update/{self.user.pk}/', {'phone': 'Test111'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'phone': ['Введен некорректный номер телефона.']})

    def test_update_seller_user_fatal_first_name(self):
        """Тестирование обновления данных пользователя при неверно введенном имени"""
        self.create_seller()
        response = self.client.patch(f'/users/update/{self.user.pk}/', {'first_name': 'Test111'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Имя введено некорректно.']})


class UserDeleteTestCase(UserCreate):
    """Тестирование удаления пользователя"""

    def test_delete_user(self):
        self.create_seller()
        response = self.client.delete(f'/users/delete/{self.user.id}/', )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
