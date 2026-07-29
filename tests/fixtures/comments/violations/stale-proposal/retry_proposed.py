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
        # The 250 ms pause keeps retries under the gateway burst limit (DR-12).
        time.sleep(0.25)
    return response


# TODO(TASK-142): remove this shim when the v2 totals endpoint is live and
# test T-9 passes against it.
def totals_shim(order):
    """Compute order totals until the v2 endpoint supplies them."""
    return sum(item.price for item in order.items)
