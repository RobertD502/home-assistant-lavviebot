""" Utilities for Purrsong Integration """
from __future__ import annotations

from typing import Any

import async_timeout
from lavviebot import LavviebotClient
from lavviebot.exceptions import LavviebotAuthError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import LOGGER, LAVVIEBOT_ERRORS, TIMEOUT

async def async_validate_api(hass: HomeAssistant, email: str, password: str) -> str:
    """ Get data from API. """
    client = LavviebotClient(
        email,
        password,
        session=async_get_clientsession(hass),
        timeout=TIMEOUT,
    )

    try:
        async with async_timeout.timeout(TIMEOUT):
            user_id_query = await client.login()
            litter_box_query = await client.async_discover_litter_boxes()
    except LavviebotAuthError as err:
        LOGGER.error(f'Could not authenticate on PurrSong servers: {err}')
        raise LavviebotAuthError from err
    except LAVVIEBOT_ERRORS as err:
        LOGGER.error(f'Failed to get information from PurrSong servers: {err}')
        raise ConnectionError from err

    user_id: int = user_id_query
    litter_boxes = litter_box_query['data']
    if not user_id:
        LOGGER.error("Could not retrieve User ID from PurrSong servers")
        raise NoUserIdError
    if not litter_boxes:
        LOGGER.error('Could not retrieve any litter boxes from PurrSong servers')
        raise NoLitterBoxesError
    return str(user_id)


class NoUserIdError(Exception):
    """ No User ID from PurrSong API """

class NoLitterBoxesError(Exception):
    """ No Litter Boxes from PurrSong API """
