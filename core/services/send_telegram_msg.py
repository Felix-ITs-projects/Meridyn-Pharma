import logging

# packages
import requests

# django
from django.conf import settings
from django.shortcuts import get_object_or_404

# orders
from core.apps.orders.models import Order

logger = logging.getLogger(__name__)

# (connect, read) - telegram javob bermay qolsa, so'rov cheksiz osilib qolmasligi uchun
CONNECT_TIMEOUT = 5
READ_TIMEOUT = 30


def send_to_telegram(chat_id, order_id):
    bot_token = settings.BOT_TOKEN

    try:
        order = get_object_or_404(Order, id=order_id)

        if order.file:
            url = f"https://api.telegram.org/bot{bot_token}/sendDocument"

            with open(order.file.path, "rb") as pdf:
                files = {'document': pdf}
                data = {'chat_id': chat_id}

                response = requests.post(
                    url, data=data, files=files,
                    timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                )

            return True

    except Exception as e:
        logger.warning("Telegram xatolik (order=%s): %s", order_id, e)
        return False


def send_message(chat_id, message):
    bot_token = settings.BOT_TOKEN

    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message
        }
        response = requests.post(
            url, data=data, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
        return True
    except Exception as e:
        logger.warning("Telegram xatosi (chat_id=%s): %s", chat_id, e)
        return False
