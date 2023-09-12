from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from market.models import Product
from market.permissions import IsSeller, IsOwner
from market.serializers import ProductCustomerSerializers, ProductSellerSerializers


class ProductListAPIView(generics.ListAPIView):
    """Представление для просмотра продуктов"""
    model = Product
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от роли пользователя"""
        if self.request.user.role == 'SELLER':
            return ProductSellerSerializers
        else:
            return ProductCustomerSerializers

    def get_queryset(self):
        """Пользователь может видеть только опубликованные привычки"""
        user = self.request.user
        if user.is_staff:
            return Product.objects.all()
        else:
            return Product.objects.filter(is_published=True)


class ProductCreateAPIView(generics.CreateAPIView):
    """Представление для добавления товара (добавлять может только пользователь-продавец)"""
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSellerSerializers
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        """Привязка пользователя к добавленному товару"""
        serializer.save(owner=self.request.user)


class ProductRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для просмотра одного товара"""
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductCustomerSerializers
    permission_classes = [IsAuthenticated]


class ProductUpdateAPIView(generics.UpdateAPIView):
    """Представление для обновления продукта (обновлять может только пользователь-создатель товара)"""
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductSellerSerializers
    permission_classes = [IsOwner]


class ProductDestroyAPIView(generics.DestroyAPIView):
    """Представление для удаления продукта (удалять может только пользователь-создатель товара)"""
    model = Product
    queryset = Product.objects.all()
    serializer_class = ProductCustomerSerializers
    permission_classes = [IsOwner]
