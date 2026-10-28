from stripe import StripeClient
from django.conf import settings

# 1. Инициализируем клиента Stripe.
# This API key belongs to a sandbox that Stripe created for you. Use this key to test the Stripe API,
# then claim the sandbox when you sign into the Dashboard.
# client = StripeClient(
#     "sk_test_51UVRBREUzW9LyDNd9nadGf7A62E2TbBrD1xwJgUgSHzUe3X5UJa1uZcoHlEHRm4EhbEdddsM0xRXl3JWL7qs8Xll006kOQ6FJz")

# Забираем ключ из настроек или подставляем фейковый для заглушки
stripe_key = getattr(
    settings,
    'STRIPE_SECRET_KEY',
    'sk_test_51UVRBREUzW9LyDNd9nadGf7A62E2TbBrD1xwJgUgSHzUe3X5UJa1uZcoHlEHRm4EhbEdddsM0xRXl3JWL7qs8Xll006kOQ6FJz'
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



# Создание сессии возвращает Response:
# {
#   "id": "cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u",
#   "object": "checkout.session",
#   "after_expiration": null,
#   "allow_promotion_codes": null,
#   "amount_subtotal": 2198,
#   "amount_total": 2198,
#   "automatic_tax": {
#     "enabled": false,
#     "liability": null,
#     "status": null
#   },
#   "billing_address_collection": null,
#   "cancel_url": null,
#   "client_reference_id": null,
#   "consent": null,
#   "consent_collection": null,
#   "created": 1679600215,
#   "currency": "usd",
#   "custom_fields": [],
#   "custom_text": {
#     "shipping_address": null,
#     "submit": null
#   },
#   "customer": null,
#   "customer_creation": "if_required",
#   "customer_details": null,
#   "customer_email": null,
#   "expires_at": 1679686615,
#   "invoice": null,
#   "invoice_creation": {
#     "enabled": false,
#     "invoice_data": {
#       "account_tax_ids": null,
#       "custom_fields": null,
#       "description": null,
#       "footer": null,
#       "issuer": null,
#       "metadata": {},
#       "rendering_options": null
#     }
#   },
#   "livemode": false,
#   "locale": null,
#   "metadata": {},
#   "mode": "payment",
#   "payment_intent": null,
#   "payment_link": null,
#   "payment_method_collection": "always",
#   "payment_method_options": {},
#   "payment_method_types": [
#     "card"
#   ],
#   "payment_status": "unpaid",
#   "phone_number_collection": {
#     "enabled": false
#   },
#   "recovered_from": null,
#   "setup_intent": null,
#   "shipping_address_collection": null,
#   "shipping_cost": null,
#   "shipping_details": null,
#   "shipping_options": [],
#   "status": "open",
#   "submit_type": null,
#   "subscription": null,
#   "success_url": "https://example.com/success",
#   "total_details": {
#     "amount_discount": 0,
#     "amount_shipping": 0,
#     "amount_tax": 0
#   },
#   "return_url": null,
#   "ui_mode": "hosted_page",
#   "url": "https://checkout.stripe.com/c/pay/cs_test_a11YYufWQzNY63zpQ6QSNRQhkUpVph4WRmzW0zWJO2znZKdVujZ0N0S22u#fidkdWxOYHwnPyd1blpxYHZxWjA0SDdPUW5JbmFMck1wMmx9N2BLZjFEfGRUNWhqTmJ%2FM2F8bUA2SDRySkFdUV81T1BSV0YxcWJcTUJcYW5rSzN3dzBLPUE0TzRKTTxzNFBjPWZEX1NKSkxpNTVjRjN8VHE0YicpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl"
# }
