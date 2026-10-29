from stripe import StripeClient
from django.conf import settings

# 1. Инициализируем клиента Stripe.
# This API key belongs to a sandbox that Stripe created for you. Use this key to test the Stripe API,
# then claim the sandbox when you sign into the Dashboard.
# client = StripeClient(
#     'sk_test_fake_key_for_safety_checking')

# Забираем ключ из настроек или подставляем фейковый для заглушки
stripe_key = getattr(
    settings,
    'STRIPE_SECRET_KEY',
    'sk_test_fake_key_for_safety_checking'
)
client = StripeClient(stripe_key)


# 2. Создаем продукт Stripe.
def create_stripe_product(name: str) -> str:
    """
    Создает продукт в Stripe
    """

    try:
        # Оригинальный код документации Stripe:
        # product = client.v1.products.create({"name": "Gold Plan"})
        # return product.id # Из сырого JSON ответа берем только нужное

        # Заглушка: возвращаем сгенерированный hash фейковый ID продукта
        fake_product_id = f"prod_fake_{hash(name)}"
        return fake_product_id

    except Exception as e:
        return f"error_product_{str(e)}"


# 3. Создаем цену Stripe.
def create_stripe_price(amount: int, product_id: str) -> str:
    """
    Создает цену в Stripe (Сумму в рублях переводим в копейки)
    """

    try:
        amount_in_cents = int(amount * 100)

        # Оригинальный код по документации Stripe:
        # price = client.v1.prices.create({
        #     "currency": "rub",
        #     "unit_amount": amount_in_cents,
        #     "product": product_id,
        # })
        # return price.id # Из сырого JSON ответа берем только нужное

        # Заглушка: возвращаем сгенерированный hash фейковый ID цены
        fake_price_id = f"price_{amount_in_cents}_{hash(product_id)}"
        return fake_price_id

    except Exception as e:
        return f"error_price_{str(e)}"


# 4. Создаем сессию Stripe.
def create_stripe_session(price_id: str) -> tuple[str, str]:
    """
    Создает сессию оплаты в Stripe и возвращает (URL ссылки, ID сессии)
    """

    try:
        # Оригинальный код по документации Stripe:
        # session = client.v1.checkout.sessions.create({
        #     "success_url": "http://127.0.0",
        #     "line_items": [{"price": price_id, "quantity": 1}],
        #     "mode": "payment",
        # })
        # return session.url, session.id # Из сырого JSON ответа берем только нужное

        # Заглушка: возвращаем что-то похожее на «живой» проект, где этот адрес полностью формируется на стороне
        # Stripe, а код на Django просто ловит его из ответа сервера и передает на фронтенд, чтобы у пользователя
        # открылось окно оплаты.
        demo_stripe_url = "https://stripe.com"

        # Заглушка: возвращаем сгенерированный hash фейковый ID сессии
        fake_session_id = f"cs_test_{hash(price_id)}"
        return demo_stripe_url, fake_session_id

    except Exception as e:
        return "", f"error_session_{str(e)}"
