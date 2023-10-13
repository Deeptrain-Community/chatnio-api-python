# Desc: Authentication for Chat Nio
from .globals import client, AuthenticationError

TOKEN = ""


def get_token() -> str:
    """
    Get the token for the Chat Nio API
    """

    return TOKEN


def set_key(token: str) -> str:
    """
    Set the token for the Chat Nio API
    :param token: The token to set for the api (e.g. "sk-...")
    :return: The token that was set
    """

    global TOKEN
    TOKEN = token
    client.headers["Authorization"] = f"Bearer {TOKEN}"

    return TOKEN


def set_key_from_env(env: str = "CHATNIO_TOKEN") -> str:
    """
    Set the token for the Chat Nio API from an environment variable
    :param env: The environment variable to get the token (default: CHATNIO_TOKEN)
    :return: The token that was set
    """

    import os
    return set_key(os.environ.get(env, ""))


def clear_key() -> None:
    """
    Clear the token for the Chat Nio API
    """

    set_key("")


def is_authenticated() -> bool:
    """
    Check if the user is authenticated (not establishment)
    :return: The authentication status of the user (True if authenticated)
    """

    return TOKEN.strip() != ""


def authenticate_require() -> None:
    """
    Raise an error if the user is not authenticated
    """

    if not is_authenticated():
        raise AuthenticationError()
