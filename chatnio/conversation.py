# Desc: Conversation Operations for Chat Nio
import json
from typing import List
from .auth import is_authenticated, authenticate_require
from .globals import client, AuthenticationError


class Message(object):
    """
    The message object for the Chat Nio API
    """
    role: str
    content: str

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    @property
    def format(self) -> dict:
        """
        Format the message for the Chat Nio API
        :return: The formatted message
        """

        return {
            "role": self.role,
            "content": self.content
        }

    def json_format(self) -> str:
        return json.dumps(self.format)

    def __str__(self):
        return f"Message(role={self.role}, content={self.content})"

    __repr__ = __str__

    def __bool__(self):
        return self.content.strip() != ""

    def __len__(self):
        return len(self.content)

    def __eq__(self, other: "Message"):
        return self.role == other.role and self.content == other.content

    def __ne__(self, other: "Message"):
        return not self.__eq__(other)

    @staticmethod
    def parse(data: dict) -> "Message":
        """
        Parse a message from the Chat Nio API
        :param data: The data to parse from the Chat Nio API
        :return: The parsed message
        """

        return Message(
            data.get("role", "user"),
            data.get("content", ""),
        )

    @staticmethod
    def parse_list(data: List[dict]) -> List["Message"]:
        """
        Parse a list of messages from the Chat Nio API
        :param data: The data to parse from the Chat Nio API
        :return: The parsed list of messages
        """

        if not isinstance(data, list):
            # fix type checking
            return []

        return [Message.parse(message) for message in data]


class Conversation(object):
    """
    The conversation object for the Chat Nio API

    Attributes:
        id (int): The id of the conversation
        name (str): The name of the conversation
        messages (list): The messages in the conversation
        length (int): The length of the conversation (number of messages)
    """

    id: int
    name: str
    messages: List[Message]
    length: int

    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.messages = Message.parse_list(data.get("messages", data.get("message", [])))

    def __str__(self):
        return f"Conversation(id={self.id}, name={self.name}, length={self.length})"

    __repr__ = __str__

    @property
    def length(self):
        return len(self.messages)

    @length.setter
    def length(self, value):
        self.messages = self.messages[:value]

    def get_messages(self, limit: int = None) -> List[Message]:
        """
        Get the messages in the conversation
        :param limit: The limit of messages to get (default: Infinity)
        :return: The messages in the conversation
        """

        if limit is None:
            return self.messages
        return self.messages[:limit]

    def insert_message(self, message: Message) -> None:
        """
        Insert a message into the conversation
        :param message: The message to insert into the conversation
        """

        self.messages.insert(0, message)

    def insert_messages(self, messages: List[Message]) -> None:
        """
        Insert messages into the conversation
        :param messages: The messages to insert into the conversation
        """

        for message in messages:
            self.insert_message(message)

    def append_message(self, message: Message) -> None:
        """
        Append a message into the conversation
        :param message: The message to append into the conversation
        """

        self.messages.append(message)

    def append_messages(self, messages: List[Message]) -> None:
        """
        Append messages into the conversation
        :param messages: The messages to append into the conversation
        """

        for message in messages:
            self.append_message(message)

    def delete_message(self, index: int) -> None:
        """
        Delete a message from the conversation
        :param index: The index of the message to delete
        """

        del self.messages[index]

    def delete_messages(self, start: int, end: int) -> None:
        """
        Delete messages from the conversation
        :param start: The start index of the messages to delete
        :param end: The end index of the messages to delete
        """

        del self.messages[start:end]

    def __bool__(self):
        return self.length > 0

    def __getitem__(self, item):
        return self.messages[item]

    def __len__(self):
        return len(self.messages)

    def __iter__(self):
        return iter(self.messages)

    def __contains__(self, item):
        return item in self.messages

    def __reversed__(self):
        return reversed(self.messages)

    def __add__(self, other):
        return self.messages + other

    def __radd__(self, other):
        return other + self.messages

    def __iadd__(self, other):
        self.messages += other
        return self

    def __setitem__(self, key, value):
        self.messages[key] = value

    def __delitem__(self, key):
        del self.messages[key]

    def __getslice__(self, i, j):
        return self.messages[i:j]

    def __setslice__(self, i, j, sequence):
        self.messages[i:j] = sequence

    def __delslice__(self, i, j):
        del self.messages[i:j]


def list_conversations() -> List[Conversation]:
    """
    List the conversations for the Chat Nio API
    :return: The list of conversations
    """

    authenticate_require()

    resp = client.get("/conversation/list")
    resp.raise_for_status()

    data = resp.json()
    if not data["status"]:
        raise AuthenticationError(data["message"])

    return [Conversation(conversation) for conversation in data["data"]]


def load_conversation(_id: int) -> Conversation:
    """
    Load a conversation from the Chat Nio API
    :param _id: The id of the conversation to load
    :return: The conversation that was loaded
    """

    authenticate_require()

    resp = client.get("/conversation/load", params={"id": _id})
    resp.raise_for_status()

    data = resp.json()
    if not data["status"]:
        raise AuthenticationError(data["message"])

    return Conversation(data["data"])


def delete_conversation(_id: int) -> bool:
    """
    Delete a conversation from the Chat Nio API
    :param _id: The id of the conversation to delete
    :return: The status of the deletion (True if successful)
    """

    authenticate_require()

    resp = client.get("/conversation/delete?id={}".format(_id))
    resp.raise_for_status()

    data = resp.json()
    return bool(data["status"])
