from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Payment
from payments.serializers import PaymentCreateSerializer
from payments.services import create_stripe_product, create_stripe_price, create_stripe_session

class PaymentCreateAPIView(generics.CreateAPIView):
    """Контроллер для регистрации платежа и получения ссылки на Stripe"""
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        # Вытаскиваем данные из запроса, чтобы узнать, что покупает пользователь
        # serializer.validated_data содержит проверенные ID курса или урока
        paid_course = serializer.validated_data.get('paid_course')
        paid_lesson = serializer.validated_data.get('paid_lesson')

        # Проверяем, за что именно платит пользователь, и берем стоимость товара
        if paid_course:
            product_name = f"Курс: {paid_course.title}" # Название курса
            amount = paid_course.price # Цена конкретного курса
        elif paid_lesson:
            product_name = f"Урок: {paid_lesson.title}"  # Название урока
            amount = paid_lesson.price  # Цена конкретного урока
        else:
            product_name = 'Оплата услуг обучения'
            amount = 100

        # Сохраняем платеж в БД, автоматически привязывая его к текущему авторизованному пользователю
        # и одновременно кладем объект(экземпляр) класса модели Payment в переменную payment
        payment = serializer.save(
            user=self.request.user,
            payment_method='TRANSFER',
            amount = amount
        )

        # Вызываем по цепочке функции из services.py Stripe (заглушек)
        product_id = create_stripe_product(product_name)
        price_id  = create_stripe_price(amount, product_id)
        payment_link, session_id = create_stripe_session(price_id)

        # Записываем сгенерированные ссылки и ID обратно в объект платежа
        payment.payment_link = payment_link
        payment.stripe_session_id = session_id
        payment.save()

    def create(self, request, *args, **kwargs):
        """Переопределяем метод ответа, чтобы сразу вернуть ссылку пользователю в JSON"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Забираем только что сохраненный объект из сериализатора
        payment_instance: Payment = serializer.instance

        return Response(
            {
                "message": "Ссылка на оплату успешно сформирована",
                "payment_link": payment_instance.payment_link,
                "stripe_session_id": payment_instance.stripe_session_id,
                "amount": payment_instance.amount
            },
            status=status.HTTP_201_CREATED
        )