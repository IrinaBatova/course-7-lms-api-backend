from  rest_framework import serializers
from users.models import Payment
from django.contrib.auth import get_user_model


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели пользователя.

    Обеспечивает вывод основных полей профиля. Поле 'password' настроено
    строго на запись (write_only), что исключает утечку хеша пароля в JSON-ответах.
    При создании пользователя автоматически вызывается метод 'create_user',
    который обеспечивает корректное хеширование пароля в базе данных.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        # Безопасность
        extra_kwargs = {
            'password': {'write_only': True}  # Чтобы пароль не возвращался в JSON-ответах
        }

    def create(self, validated_data):
        """
        Переопределяем стандартный метод create. Связка с логикой модели
        """
        # Метод create_user (переопределен в кастомном менеджере в models.py)
        # автоматически захеширует пароль перед сохранением в базу данны
        user = User.objects.create_user(**validated_data)
        return user

class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для объектов модели Payment (Платеж). Переводит все поля объекта в JSON (сериализация)
    и после проверки (валидация) обратно в Python (десериализация).
    """
    class Meta:
        model = Payment
        fields = '__all__'