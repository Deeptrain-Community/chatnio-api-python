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


class AuthenticationError(Exception):
    def __init__(self, message: str = "Authentication Error"):
        super().__init__(message)
