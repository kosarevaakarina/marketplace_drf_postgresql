import re
from rest_framework import serializers
from market.models import Product


class ProductSellerSerializers(serializers.ModelSerializer):
    """Сериализатор представления товара (для использования пользователями-продавцами)"""
    class Meta:
        model = Product
        fields = ('title', 'description', 'cost_price', 'price', 'image')

    def create(self, validated_data):
        """Добавление нового товара"""
        cost_price = validated_data.get('cost_price')
        price = cost_price * 1.06 * 1.02 * 1.20
        product = Product.objects.create(**validated_data, price=price)
        return product

    def update(self, instance, validated_data):
        """Обновление данных о продукте"""
        super().update(instance, validated_data)
        if 'cost_price' in validated_data:
            cost_price = self.validated_data.get('cost_price')
            instance.cost_price = self.validated_data.get('cost_price')
            instance.price = cost_price * 1.06 * 1.02 * 1.20
            instance.save()
        return instance

    def validate(self, attrs):
        """Валидация данных при добавлении и обновлении товара"""
        title = attrs.get('title', None)
        cost_price = attrs.get('cost_price', None)
        description = attrs.get('description', None)
        if 'title' in attrs:
            tpl = r'[а-яА-Яa-zA-Z0-9 -]*'
            if not re.fullmatch(tpl, title):
                raise serializers.ValidationError(
                    'Некорректное название товара. Недопустимо использование посторонних символов')
        if 'cost_price' in attrs:
            if cost_price <= 0:
                raise serializers.ValidationError('Себестоимость товара не может быть меньше нуля')
        if Product.objects.filter(title=title, description=description, cost_price=cost_price).exists():
            raise serializers.ValidationError(
                'Товар с таким названием, ценой и описанием уже существует')
        return attrs


class ProductCustomerSerializers(serializers.ModelSerializer):
    """Сериализатор представления товара (для использования пользователями-покупателями)"""
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'image')
