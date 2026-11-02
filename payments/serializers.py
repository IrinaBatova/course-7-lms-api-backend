from rest_framework import serializers
from users.models import Payment

class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        # Пользователь при запросе укажет только то, что он хочет купить (курс или урок)
        fields = ('paid_course', 'paid_lesson',)