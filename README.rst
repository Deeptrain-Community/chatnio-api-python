======================
ChatNio Python Library
======================


The official Python library for the Chat Nio API

* Authors: Deeptrain Team
* Free software: MIT license
* Documentation: https://docs.chatnio.net

Features
========

* Chat
* Conversation
* Quota
* Subscription and Package


Installation
============

Install using `pip`

.. code-block:: bash

    pip install --upgrade chatnio

And then import it

.. code-block:: python

    import chatnio


Usage
=====

* Authentication

.. code-block:: python

    chatnio.set_key("sk-...")
    # or read from environment variable
    chatnio.set_key_from_env("CHATNIO_TOKEN")

    # set custom api endpoint (default: https://api.chatnio.net)
    # chatnio.set_endpoint("https://example.com/api")

    # clear token
    chatnio.clear_key()

    # get current token
    chatnio.get_token()


* Chat

.. code-block:: python

    chat = await chatnio.new_chat()

    async for message in chat.ask("Hello, world!"):
        print(message.message, end="")


* Conversation

.. code-block:: python

    # list conversations (100 conversations max)
    for conversation in chatnio.list_conversations():
        print(conversation.id, conversation.name)

    # load conversation
    conversation = chatnio.load_conversation(42)
    print(conversation)
    for message in conversation.messages:
        print(message.role, message.content)

    # delete conversation
    state = chatnio.delete_conversation(42)
    print(state)


* Quota

.. code-block:: python

    # get quota
    quota = chatnio.get_quota()
    print(quota)

    # buy quota
    state = chatnio.buy_quota(1000)
    print(state)


* Subscription and Package

.. code-block:: python

    # get subscription
    subscription = chatnio.get_subscription()
    print(subscription.is_subscribed, subscription.expired)

    # buy subscription
    state = chatnio.buy_subscription(1, 1) # 1 month of basic plan
    print(state)

    # get package
    package = chatnio.get_package()
    print(package)


* Error

    chatnio.AuthenticationError


Test
====

To run the tests, you need to set the environment variable `CHATNIO_TOKEN` to your secret key.

.. code-block:: bash

    export CHATNIO_TOKEN="sk-..."

Then run the tests

.. code-block:: bash

    pytest

