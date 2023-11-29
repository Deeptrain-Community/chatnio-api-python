import logging
from chatnio import get_quota, buy_quota, get_package, get_subscription, buy_subscription, Subscription


def test_get_quota():
    quota = get_quota()
    logging.debug(f"[quota]: get current quota: {quota}")
    assert quota >= 0


def _test_buy_quota():
    result = buy_quota(1)
    logging.debug(f"[quota]: buy quota: {result}")

    assert result


def test_get_package():
    result = get_package()
    logging.debug(f"[quota]: get package: {result}")

    assert isinstance(result, dict)
    assert "cert" in result and "teenager" in result


def test_get_subscription():
    result = get_subscription()
    logging.debug(f"[quota]: get subscription: {result}")

    assert isinstance(result, Subscription)
    assert hasattr(result, "is_subscribed") and hasattr(result, "expired")


def _test_buy_subscription():
    result = buy_subscription(1, 1)
    logging.debug(f"[quota]: buy subscription: {result}")

    assert result

