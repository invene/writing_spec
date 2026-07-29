"""Retry helpers for the payment gateway client."""

import time


def send_with_retry(request, transport):
    """Send one request, retrying after a short pause."""
    retries = 0
    while retries < 5:
        response = transport.send(request)
        if response.ok:
            return response
        retries += 1
        time.sleep(0.25)
    return response


def totals_shim(order):
    """Compute order totals until the v2 endpoint supplies them."""
    return sum(item.price for item in order.items)
