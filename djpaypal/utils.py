# -*- coding: utf-8 -*-
from decimal import Decimal

from django.db.models import AutoField, BigIntegerField
from django.utils.translation import gettext_lazy as _


class BigAutoField(AutoField):
    description = _("Big (8 byte) integer")

    def db_type(self, connection):
        return "bigserial"

    def get_internal_type(self):
        return "BigAutoField"

    def rel_db_type(self, connection):
        return BigIntegerField().db_type(connection=connection)


def fix_django_headers(meta):
    """
    Fix this nonsensical API:
    https://docs.djangoproject.com/en/1.11/ref/request-response/
    https://code.djangoproject.com/ticket/20147
    """
    ret = {}
    for k, v in meta.items():
        if k.startswith("HTTP_"):
            k = k[len("HTTP_"):]
        elif k not in ("CONTENT_LENGTH", "CONTENT_TYPE"):
            # Skip CGI garbage
            continue

        ret[k.lower().replace("_", "-")] = v

    return ret


CURRENCY_SIGILS = {
    "CAD": "$",
    "EUR": "€",
    "GBP": "£",
    "USD": "$",
}


def get_friendly_currency_amount(amount, currency):
    currency = currency.upper()
    sigil = CURRENCY_SIGILS.get(currency, "")
    # Always show two decimal places on the amount
    # Note that amount is usually a string, so convert to Decimal first.
    amount = "{:.2f}".format(Decimal(amount))
    return "{sigil}{amount} {currency}".format(sigil=sigil, amount=amount, currency=currency)


def get_version():
    """
    Returns the current dj-paypal version
    """
    from . import __version__
    return __version__
