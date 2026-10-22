from  rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from users.models import Payment
from users.serializers import PaymentSerializer


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Подключаем встроенную фильтрацию Django и сортировку DRF
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Поля, по которым пользователь сможет фильтровать платежи
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')

    # Поля, по которым можно будет сортировать список
    ordering_fields = ('payment_date',)
