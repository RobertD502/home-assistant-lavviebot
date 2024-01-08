""" DataUpdateCoordinator for the PurrSong integration. """
from __future__ import annotations

from datetime import timedelta

from aiohttp import ClientSession
from lavviebot import LavviebotClient
from lavviebot.exceptions import LavviebotAuthError, LavviebotError, LavviebotRateLimit
from lavviebot.model import LavviebotData


from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, LOGGER, TIMEOUT

class LavviebotDataUpdateCoordinator(DataUpdateCoordinator):
    """ PurrSong Data Update Coordinator. """

    data: LavviebotData

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the PurrSong coordinator."""

        self.client = LavviebotClient(
            entry.data[CONF_EMAIL],
            entry.data[CONF_PASSWORD],
            session=ClientSession(),
            timeout=TIMEOUT,
        )
        super().__init__(
            hass,
            LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )

    async def _async_update_data(self) -> LavviebotData:
        """ Fetch data from PurrSong. """

        try:
            data = await self.client.async_get_data()
        except LavviebotAuthError as error:
            raise ConfigEntryAuthFailed(error) from error
        except LavviebotError as error:
            raise UpdateFailed(error) from error
        except LavviebotRateLimit:
            LOGGER.debug("Purrsong API has rate limited current session. Starting new ClientSession.")
            await self.client._session.close()
            self.client._session = ClientSession()
            self.client.token = None
            return await self._async_update_data()
        else:
            if not data.litterboxes:
                raise UpdateFailed("No Litter Boxes found")
            else:
                return data
