""" Utilities for Purrsong Integration """
from __future__ import annotations

from http.cookies import SimpleCookie
from typing import Any

from aiohttp import ClientSession
import async_timeout
from lavviebot import LavviebotClient
from lavviebot.exceptions import LavviebotAuthError

from .const import LOGGER, LAVVIEBOT_ERRORS, TIMEOUT


class PurrSongClient(LavviebotClient):
    """LavviebotClient subclass that fixes aiohttp SimpleCookie header compatibility."""

    async def _post(
        self,
        headers: dict[str, Any],
        payload: dict[str, Any] | list[dict[str, Any]],
        is_cookie: bool | None = None,
    ) -> SimpleCookie | dict[str, Any]:
        """Make Post API call to PurrSong servers with serialized Cookie header."""
        req_headers = dict(headers)
        cookie = req_headers.get("Cookie")
        if isinstance(cookie, SimpleCookie):
            if cookie:
                req_headers["Cookie"] = "; ".join(
                    f"{k}={v.coded_value}" for k, v in cookie.items()
                )
            else:
                req_headers.pop("Cookie", None)
        return await super()._post(req_headers, payload, is_cookie)

    async def async_discover_litter_boxes(self) -> dict[str, Any]:
        """Fix upstream typo in async_discover_devices token re-auth retry."""
        return await self.async_discover_devices()

    async def async_get_litter_box_status(self, device_id: int) -> list[dict[str, Any]]:
        """Get most recent status available for litter box, guarding against empty catUsageHistory."""
        response = await super().async_get_litter_box_status(device_id)
        try:
            poop_record = response[1]["data"]["getIotPoopRecord"]
            if poop_record is not None and not poop_record.get("catUsageHistory"):
                poop_record["catUsageHistory"] = [
                    {"nickname": "None", "duration": 0, "creationTime": "0"}
                ]
        except (IndexError, KeyError, TypeError):
            pass
        return response


async def async_validate_api(email: str, password: str) -> None:
    """ Get data from API. """
    client = PurrSongClient(
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
