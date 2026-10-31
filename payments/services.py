import stripe
from stripe import StripeClient
from django.conf import settings

# 1. Инициализируем клиента Stripe.
# Забираем ключ из настроек или подставляем фейковый для заглушки
stripe_key = getattr(
    settings,
    'STRIPE_SECRET_KEY',
    'sk_test_fake_key_for_safety_checking'
)
client = StripeClient(stripe_key)

# Записывая ключ в специальное внутреннее свойство stripe.api_key, для его использования для всех запросов
stripe.api_key = stripe_key

# 2. Создаем продукт Stripe.
def create_stripe_product(name: str) -> str:
    """
    Создает продукт в Stripe
    Если Stripe недоступен, возвращает мок-данные.
    """

    try:
        # Пробуем сделать реальный запрос
        product = stripe.Product.create(name=name)
        print(f"[Stripe REAL] Продукт '{name}' успешно создан.")
        return product.id

    except Exception as e:
        # Резервный вариант (фаллбэк) на случай ошибки
        print(f"[Stripe FALLBACK] Ошибка создания продукта ({e}). Активирован мок.")
        fake_product_id = f"prod_fake_{hash(name)}"
        return fake_product_id

# 3. Создаем цену Stripe.
def create_stripe_price(amount: int, product_id: str) -> str:
    """
    Создает цену в Stripe (Сумму в рублях переводим в копейки)
    Если Stripe недоступен, возвращает мок-данные.
    """

    try:
        amount_in_cents = int(amount * 100)

        # Пробуем сделать реальный запрос
        price = stripe.Price.create(
            currency="rub",
            unit_amount=amount_in_cents,
            product=product_id,
        )
        print(f"[Stripe REAL] Цена {amount} руб. успешно создана для продукта {product_id}.")
        return price.id

    except Exception as e:
        # Резервный вариант (фаллбэк) на случай ошибки
        amount_in_cents = int(amount * 100)
        print(f"[Stripe FALLBACK] Ошибка создания цены ({e}). Активирован мок.")
        fake_price_id = f"price_{amount_in_cents}_{hash(product_id)}"
        return fake_price_id


# 4. Создаем сессию Stripe.
def create_stripe_session(price_id: str) -> tuple[str, str]:
    """
    Создает сессию оплаты в Stripe и возвращает (URL ссылки, ID сессии)
    Если Stripe недоступен (сетевая ошибка, блокировка), возвращает мок-данные.
    """

    try:
        # Пробуем сделать реальный запрос
        session = stripe.checkout.Session.create(
            success_url="http://127.0.0",
            line_items=[{"price": price_id, "quantity": 1}],
            mode="payment",
        )

        print("[Stripe REAL] Сессия оплаты успешно создана через Stripe API.")
        return session.url, session.id

    except Exception as e:
        # Резервный вариант (фаллбэк) на случай ошибки

        print(f"[Stripe FALLBACK] Сервер Stripe недоступен ({e}). Активированы мок-данные.")

        fake_session_id = f"cs_test_{hash(price_id)}"
        demo_stripe_url = "https://stripe.com"

        return demo_stripe_url, fake_session_id
