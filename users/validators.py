from rest_framework import serializers


class FirstNameValidator:
    """Валидация имени: имя должно состоять только из букв"""
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        first_name = value.get('first_name')
        if first_name is not None and not first_name.isalpha():
            raise serializers.ValidationError('Имя введено некорректно.')


class LastNameValidator:
    """Валидация фамилии: фамилия должна состоять только из букв"""

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        last_name = value.get('last_name')
        if last_name is not None and not last_name.isalpha():
            raise serializers.ValidationError('Фамилия введена некорректно.')
