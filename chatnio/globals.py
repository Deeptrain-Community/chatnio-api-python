# Desc: Globals for Chat Nio
import httpx

API_BASE = "https://api.chatnio.net"

client = httpx.Client(
    base_url=API_BASE,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
    },
)


def set_endpoint(endpoint: str) -> None:
    """
    Set the endpoint for the Chat Nio API
    :param endpoint: The endpoint for the Chat Nio API
    """

    global API_BASE
    API_BASE = endpoint
    client.base_url = endpoint


def get_chat_url():
    # http to ws, https to wss
    return API_BASE.replace("http", "ws").replace("https", "wss") + "/chat"


class AuthenticationError(Exception):
    def __init__(self, message: str = "Authentication Error"):
        super().__init__(message)
