from rest_framework import status

from market.tests.services import UserCreate


class ProductCreateTestCase(UserCreate):
    """Тестирование добавления товара"""

    def create_product(self):
        response = self.client.post('/create/', {
            'title': 'newtest',
            'cost_price': 100,
            'description': 'another description'
        })
        return response

    def test_product_create_seller_user(self):
        """Тестирование добавления товара для пользователя-продавца"""
        self.seller_binging()
        response = self.create_product()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {
            'title': 'newtest',
            'description': 'another description',
            'cost_price': 100,
            'price': 129,
            'image': None})

    def test_product_create_customer_user(self):
        """Тестирование добвления товара для пользователя-покупателя"""
        self.customer_binging()
        response = self.create_product()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})

    def test_product_create_with_fatal_title(self):
        self.seller_binging()
        response = self.client.post('/create/', {
            'title': 'Teeest*-)',
            'cost_price': 100,
            'description': 'description'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': [
            'Некорректное название товара. Недопустимо использование посторонних символов']})

    def test_product_create_with_fatal_cost_price(self):
        self.seller_binging()
        response = self.client.post('/create/', {
            'title': 'Teeest',
            'cost_price': 0,
            'description': 'description'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': [
            'Себестоимость товара не может быть меньше нуля']})


class ProductListTestCase(UserCreate):
    """Тестирование просмотра продуктов"""

    def get_product(self):
        response = self.client.get('', )
        return response

    def test_get_product_unauth_user(self):
        """Тестирование просмотра продукта для неавторизованного пользователя"""
        response = self.get_product()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Учетные данные не были предоставлены.'})

    def test_get_product_seller_user(self):
        """Тестирование просмотра продукта для пользователя-продавца"""
        self.seller_binging()
        response = self.get_product()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{
            'title': 'test',
            'description': 'description',
            'cost_price': 1000,
            'price': 1297,
            'image': None}])

    def test_get_product_customer_user(self):
        """Тестирование просмотра продукта для пользователя-покупателя"""
        self.customer_binging()
        response = self.get_product()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{
            'title': 'test',
            'description': 'description',
            'price': 1297,
            'image': None}])


class ProductRetrieveAPITest(UserCreate):
    """Тестирование просмотра одного продукта"""

    def retrieve_product(self, product_id):
        return self.client.get(f'/{product_id}/', )

    def test_retrieve_product_seller_user(self):
        """Тестирование просмотра одного продукта для пользователя-продавца"""
        product = self.seller_binging()
        response = self.retrieve_product(product.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'title': 'test',
            'description': 'description',
            'price': 1297,
            'image': None})

    def test_retrieve_product_customer_user(self):
        """Тестирование просмотра одного продукта для пользователя-покупателя"""
        product = self.customer_binging()
        response = self.retrieve_product(product.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'title': 'test',
            'description': 'description',
            'price': 1297,
            'image': None})


class ProductUpdateTestCase(UserCreate):
    """Тестирование обновления продукта"""

    def update_product(self, product_id):
        return self.client.patch(f'/update/{product_id}/', {'cost_price': 1800})

    def test_update_product_seller_user(self):
        """Тестирование обновления продукта для пользователя-продавца"""
        product = self.seller_binging()
        response = self.update_product(product.pk)
        self.assertEqual(response.json(), {
            'title': 'test',
            'description': 'description',
            'cost_price': 1800,
            'price': 2335,
            'image': None})

    def test_update_product_customer_user(self):
        """Тестирование обновления продукта для пользователя-продавца"""
        product = self.customer_binging()
        response = self.update_product(product.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})


class ProductDeleteTestCase(UserCreate):
    """Тестирование удаления продукта"""

    def delete_course(self, product_id):
        return self.client.delete(f'/delete/{product_id}/', )

    def test_delete_product_seller_user(self):
        """Тестирование удаления продукта для пользователя-продавца"""
        product = self.seller_binging()
        response = self.delete_course(product.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_customer_user(self):
        """Тестирование удаления продукта для пользователя-продавца"""
        product = self.customer_binging()
        response = self.delete_course(product.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'У вас недостаточно прав для выполнения данного действия.'})
