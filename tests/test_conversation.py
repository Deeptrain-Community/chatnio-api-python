import logging
from chatnio import list_conversations, load_conversation, delete_conversation, Conversation


def test_list_conversations():
    conversations = list_conversations()
    logging.info(f"[conversation]: load conversations: {conversations}")

    assert isinstance(conversations, list)
    assert all(isinstance(conversation, Conversation) for conversation in conversations)


def test_load_conversation():
    conversation = load_conversation(1)
    logging.info(f"[conversation]: load conversation: {conversation}")

    assert isinstance(conversation, Conversation)
    assert conversation.id == 1


def _test_delete_conversation():
    result = delete_conversation(4)
    logging.info(f"[conversation]: delete conversation: {result}")

    assert result
