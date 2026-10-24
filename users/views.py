from rest_framework.generics import ListAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from users.models import Payment
from users.serializers import PaymentSerializer, UserSerializer

User = get_user_model()

class UserViewSet(ModelViewSet):
    """ Контроллер реализует CRUD для пользователей"""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Динамические права: Переопределение метода get_permissions(), настраиваем права доступа:
        - Создание пользователя (регистрация) доступно ВСЕМ (AllowAny).
        - Остальные действия (список, просмотр, изменения) только АВТОРИЗОВАННЫМ (IsAuthenticated).
        """
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

class PaymentListAPIView(ListAPIView):
    """Контроллер для создания списка платежей пользователя, с возможностью фильтрации и сортировки."""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Подключаем встроенную фильтрацию Django и сортировку DRF
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Поля, по которым пользователь сможет фильтровать платежи
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method')

    # Поля, по которым можно будет сортировать список
    ordering_fields = ('payment_date',)
