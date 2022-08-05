""" Constants for PurrSong """

import asyncio
import logging

from aiohttp.client_exceptions import ClientConnectionError
from lavviebot.exceptions import LavviebotAuthError, LavviebotError

from homeassistant.const import Platform

LOGGER = logging.getLogger(__package__)

DEFAULT_SCAN_INTERVAL = 60
DOMAIN = "purrsong"
PLATFORMS = [
    Platform.BINARY_SENSOR,
    Platform.SENSOR,
    Platform.UPDATE,
]

DEFAULT_NAME = "PurrSong"
TIMEOUT = 8

LAVVIEBOT_ERRORS = (
    ClientConnectionError,
    asyncio.TimeoutError,
    LavviebotAuthError,
    LavviebotError,
)
