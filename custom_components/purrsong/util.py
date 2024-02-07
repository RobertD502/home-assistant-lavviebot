""" Utilities for Purrsong Integration """
from __future__ import annotations

from typing import Any

from aiohttp import ClientSession
import async_timeout
from lavviebot import LavviebotClient
from lavviebot.exceptions import LavviebotAuthError

from .const import LOGGER, LAVVIEBOT_ERRORS, TIMEOUT

async def async_validate_api(email: str, password: str) -> None:
    """ Get data from API. """
    client = LavviebotClient(
        email,
        password,
        session=ClientSession(),
        timeout=TIMEOUT,
    )

    try:
        async with async_timeout.timeout(TIMEOUT):
            devices_query = await client.async_get_data()
    except LavviebotAuthError as err:
        LOGGER.error(f'Could not authenticate on PurrSong servers: {err}')
        raise LavviebotAuthError from err
    except LAVVIEBOT_ERRORS as err:
        LOGGER.error(f'Failed to get information from PurrSong servers: {err}')
        raise ConnectionError from err
    else:
        devices = [devices_query.lavvie_scanners, devices_query.lavvie_tags, devices_query.litterboxes]
        if all(not d for d in devices):
            LOGGER.error('Could not retrieve any devices from PurrSong servers')
            raise NoDevicesError       
    finally:
        await client._session.close()


class NoDevicesError(Exception):
    """ No Devices from PurrSong API """
