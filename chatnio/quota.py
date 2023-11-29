# Desc: Quota Operations for Chat Nio
from .auth import authenticate_require, is_authenticated
from .globals import client, AuthenticationError


class Subscription(object):
    """
    The subscription status for the Chat Nio API

    Attributes:
        is_subscribed (bool): The subscription status of the user
        expired (int): The expiration date of the subscription (days)
    """

    is_subscribed = False
    expired = 0

    def __init__(self, data: dict):
        self.is_subscribed = bool(data["is_subscribed"])
        self.expired = int(data["expired"])

    def __bool__(self):
        return self.is_subscribed

    def __int__(self):
        return self.expired

    def __str__(self):
        return f"Subscription(is_subscribed={self.is_subscribed}, expired={self.expired})"

    __repr__ = __str__


def get_quota() -> float:
    """
    Get the quota for the Chat Nio API
    :return: The quota for the Chat Nio API
    """

    if not is_authenticated():
        return 0.

    resp = client.get("/quota")
    resp.raise_for_status()

    data = resp.json()
    if not data["status"]:
        raise AuthenticationError(data["message"])

    return float(data["quota"])


def buy_quota(quota: int) -> bool:
    """
    Buy quota for the Chat Nio API
    :param quota: The quota to buy for the Chat Nio API
    :return: The status of the purchase (True if successful)
    """

    authenticate_require()

    if quota <= 0:
        raise ValueError("Quota must be greater than 0")

    resp = client.post("/buy", json={"quota": quota})
    resp.raise_for_status()

    data = resp.json()
    return bool(data["status"])


def get_subscription() -> Subscription:
    """
    Get the subscription status for the Chat Nio API
    :return: The `subscription` instance
    """

    if not is_authenticated():
        return Subscription({"is_subscribed": False, "expired": 0})

    resp = client.get("/subscription")
    resp.raise_for_status()

    data = resp.json()
    if not data["status"]:
        raise AuthenticationError(data["message"])

    return Subscription(data)


def buy_subscription(level: int, month: int) -> bool:
    """
    Buy subscription for the Chat Nio API
    :return: The status of the purchase (True if successful)
    """

    authenticate_require()

    if month <= 0:
        raise ValueError("Month must be greater than 0")
    resp = client.post("/subscribe", json={"level": level, "month": month})
    resp.raise_for_status()

    data = resp.json()
    return bool(data["status"])


def get_package() -> dict:
    """
    Get the package for the Chat Nio API
    :return: The package for the Chat Nio API
    :rtype: dict

    Returns example:
    {
        "cert": True,
        "teenager": True
    }
    """

    if not is_authenticated():
        return {"cert": False, "teenager": False}

    resp = client.get("/package")
    resp.raise_for_status()

    data = resp.json()
    if not data["status"]:
        raise AuthenticationError(data["message"])

    return data["data"]
