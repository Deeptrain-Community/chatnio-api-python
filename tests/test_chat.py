import logging
from chatnio import new_chat, Chat, PartialMessage


async def _test_new_chat():
    chat = await new_chat()
    logging.debug(f"[chat]: new chat: {chat}")

    assert isinstance(chat, Chat)
    assert chat.id == -1

    async for message in chat.ask("Hello, world!"):
        logging.debug(f"[chat]: new message: {message}")
        assert isinstance(message, PartialMessage)


def test_new_chat():
    import asyncio
    asyncio.run(_test_new_chat())
