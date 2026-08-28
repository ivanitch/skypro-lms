import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    """Создает продукт в Stripe."""
    return stripe.Product.create(name=name)


def create_stripe_price(amount, product_id):
    """Создает цену в копейках и привязывает к продукту."""
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),  # Обязательный перевод в копейки
        product=product_id,
    )


def create_stripe_session(price_id):
    """Создает сессию на оплату."""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8090/",  # URL для редиректа после успешной оплаты
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
