""" Utilities for Purrsong Integration """
from __future__ import annotations

from http.cookies import SimpleCookie
import time
from typing import Any

from aiohttp import ClientSession
import async_timeout
from lavviebot import LavviebotClient
from lavviebot.exceptions import LavviebotAuthError, LavviebotError, LavviebotRateLimit
from lavviebot.model import LavviebotData

from .const import LOGGER, LAVVIEBOT_ERRORS, TIMEOUT

LOGIN_COOLDOWN_SECONDS = 300
_LOGIN_COOLDOWN_UNTIL: dict[str, float] = {}


class PurrSongClient(LavviebotClient):
    """LavviebotClient subclass that fixes aiohttp SimpleCookie header compatibility and login loops."""

    def __init__(
        self,
        email: str,
        password: str,
        session: ClientSession | None = None,
        timeout: int = TIMEOUT,
    ) -> None:
        super().__init__(email, password, session=session, timeout=timeout)
        self._logged_in_this_cycle: bool = False

    async def login(self) -> None:
        """Get fresh cookie and token, enforcing rate-limit cooldown and preventing recursive loops."""
        now = time.monotonic()
        cooldown_until = _LOGIN_COOLDOWN_UNTIL.get(self.email, 0.0)
        if now < cooldown_until:
            remaining = int(cooldown_until - now)
            raise LavviebotRateLimit(
                f"PurrSong login rate-limited; cooling down for {remaining}s before retrying."
            )

        if self._logged_in_this_cycle:
            raise LavviebotError(
                "PurrSong API requested re-login again within the same update cycle; aborting to prevent login loop."
            )

        self._logged_in_this_cycle = True
        self._session.cookie_jar.clear()
        self.cookie = None
        self.token = None
        await super().login()

    async def async_get_data(self) -> LavviebotData:
        """Return dataclass with litter boxes and cats associated with account."""
        self._logged_in_this_cycle = False
        return await super().async_get_data()

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
        try:
            return await super()._post(req_headers, payload, is_cookie)
        except LavviebotRateLimit:
            _LOGIN_COOLDOWN_UNTIL[self.email] = time.monotonic() + LOGIN_COOLDOWN_SECONDS
            raise
        except LavviebotError as err:
            if "Too many login attempts" in str(err) or "Too many requests" in str(err):
                _LOGIN_COOLDOWN_UNTIL[self.email] = time.monotonic() + LOGIN_COOLDOWN_SECONDS
                raise LavviebotRateLimit(str(err)) from err
            raise

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
