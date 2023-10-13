from .auth import (
    get_token,
    set_key,
    set_key_from_env,
    clear_key,
    is_authenticated,
)

from .quota import (
    Subscription,
    get_subscription,
    buy_subscription,
    get_quota,
    buy_quota,
    get_package,
)

from .globals import *

__version__ = '0.0.1'
__author__ = 'Deeptrain Community'
__all__ = [
    'AuthenticationError',

    'get_token',
    'set_key',
    'set_key_from_env',
    'clear_key',
    'is_authenticated',

    'Subscription',
    'get_quota',
    'buy_quota',
    'get_package',
    'get_subscription',
    'buy_subscription',
]
