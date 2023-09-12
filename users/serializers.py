from rest_framework import serializers
from users.models import User
from users.validators import FirstNameValidator, LastNameValidator


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'role')
        validators = [FirstNameValidator(field='first_name'), LastNameValidator(field='last_name')]


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password2 = serializers.CharField()
    validators = [FirstNameValidator(field='first_name'), LastNameValidator(field='last_name')]

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'role', 'password', 'password2']

    def save(self, *args, **kwargs):
        """Метод для сохранения нового пользователя"""
        # Проверка на валидность пароли
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        # Если пароли не валидны, то возбуждение ошибки
        if password != password2:
            raise serializers.ValidationError("Password doesn't match")
        # Создание пользователя
        user = User.objects.create(
            email=self.validated_data.get('email'),
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            phone=self.validated_data.get('phone'),
            role=self.validated_data.get('role')
        )
        # Сохраняем пароль
        user.set_password(password)
        user.save()
        return user
