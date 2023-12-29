# Desc: Chat Connection for Chat Nio
import json
from typing import AsyncGenerator
import websockets

from .globals import get_chat_url
from .auth import is_authenticated, get_token


class PartialMessage(object):
    """
    The partial message object for the Chat Nio API
    """

    message: str
    keyword: str
    quota: float
    end: bool

    def __init__(self, data: dict):
        self.message = data.get("message", "")
        self.keyword = data.get("keyword", "")
        self.quota = float(data.get("quota", 0.))
        self.end = bool(data.get("end", False))

    def __str__(self):
        return (
            f"PartialMessage"
            f"(message=\"{self.message}\", keyword=\"{self.keyword}\", quota={self.quota}, end={self.end})"
        )

    __repr__ = __str__

    def __bool__(self):
        return self.message.strip() != ""

    def __len__(self):
        return len(self.message)


class Chat(object):
    """
    The chat connection for the Chat Nio API
    """
    id: int
    token: str
    connection: websockets.WebSocketClientProtocol = None

    def __init__(self, conversation_id: int = -1):
        self.id = conversation_id
        self.uri = get_chat_url()
        self._waiting = False

    @property
    def token(self):
        return "anonymous" if not is_authenticated() else get_token()

    async def connect(self) -> None:
        self.connection = await websockets.connect(self.uri)

        return await self.send({
            "id": self.id,
            "token": self.token,
        })

    def is_connected(self) -> bool:
        return self.connection is not None

    def raise_if_not_connected(self) -> None:
        if not self.is_connected():
            raise ConnectionError("Not connected to chat server ({}).".format(self.uri))

    def close(self) -> bool:
        if self.is_connected():
            self.connection.close()
            return True
        return False

    async def send(self, message: any) -> None:
        self.raise_if_not_connected()

        if not isinstance(message, str):
            message = json.dumps(message)
        await self.connection.send(message)

    async def receive(self) -> PartialMessage:
        self.raise_if_not_connected()

        response = await self.connection.recv()
        if not isinstance(response, dict):
            response = json.loads(response)
        return PartialMessage(response)

    async def send_message(self, message: str, model: str = "gpt-3.5-turbo", web: bool = False) -> None:
        """
        Send a message to the Chat Nio API
        :param message: The message to send to the Chat Nio API
        :param model: The model to use (default: "gpt-3.5-turbo")
        :param web: Whether to enable online searching features (default: False)

        see more at https://docs.chatnio.net/reference/api-jie-kou-can-kao/liao-tian
        """

        await self.send({
            "type": "chat",
            "message": message,
            "model": model,
            "web": web,
        })

    def _waiting_for_end(self) -> None:
        while self._waiting:
            pass

    async def ask(
        self,
        message: str,
        model: str = "gpt-3.5-turbo",
        web: bool = False,
    ) -> AsyncGenerator[PartialMessage, None]:
        """
        Ask a question to the Chat Nio API
        :param message: The message to ask
        :param model: The model to use (default: "gpt-3.5-turbo")
        :param web: Whether to enable online searching features (default: False)
        :return: The response from the Chat Nio API

        see more at https://docs.chatnio.net/reference/api-jie-kou-can-kao/liao-tian

        e.g.
        >>> chat = Chat(id=-1)
        >>> async for partial in chat.ask("hi"):
        ...     print(partial)

        PartialMessage(message="hi", keyword="", quota=0.0, end=False)
        PartialMessage(message=", ", keyword="", quota=0.0, end=False)
        PartialMessage(message="how can I ", keyword="", quota=0.0, end=False)
        PartialMessage(message="assist", keyword="", quota=0.0, end=False)
        PartialMessage(message=" you?", keyword="", quota=0.0, end=False)

        >>> print(partial.quota)
        0.0
        >>> chat.close()
        """

        if message.strip() == "":
            yield PartialMessage({"message": "", "keyword": "", "quota": 0., "end": True})
            return

        # fix: avoiding contextualization, blocked from the client
        self._waiting_for_end()
        self._waiting = True

        await self.send_message(message, model, web)
        while True:
            response = await self.receive()
            yield response

            if response.end:
                break

        self._waiting = False
        return

    def ask_sync(
        self,
        message: str,
        model: str = "gpt-3.5-turbo",
        web: bool = False,
        hook: callable = None,
    ) -> None:
        """
        Ask a question to the Chat Nio API
        :param message: The message to ask
        :param model: The model to use (default: "gpt-3.5-turbo")
        :param web: Whether to enable online searching features (default: False)
        :param hook: The hook to call when a partial message is received
        :return: The response from the Chat Nio API

        see more at https://docs.chatnio.net/reference/api-jie-kou-can-kao/liao-tian

        e.g.
        >>> chat = Chat(id=8)
        >>> chat.ask_sync("welcome", model="gpt-4", hook=lambda partial: print(partial))
        PartialMessage(message="Welcome! ", keyword="", quota=0.0, end=False)
        ...

        >>> chat.close()
        """

        if message.strip() == "":
            return

        # fix: avoiding contextualization, blocked from the client
        self._waiting_for_end()
        self._waiting = True

        async def stream():
            await self.send_message(message, model, web)
            while True:
                response = await self.receive()
                if hook is not None:
                    hook(response)

                if response.end:
                    break

            self._waiting = False
            return

        import asyncio
        asyncio.run(stream())
        return

    def __str__(self):
        return f"Chat(id={self.id}, token={self.token}, connection={self.connection})"

    __repr__ = __str__

    def __bool__(self):
        return self.is_connected()

    def __int__(self):
        return self.id


async def new_chat(conversation_id: int = -1) -> Chat:
    """
    Create a new chat connection for the Chat Nio API
    :param conversation_id: The id of the conversation to connect to (default: -1)
    :return: The `chat` instance
    """

    chat = Chat(conversation_id)
    await chat.connect()
    return chat
