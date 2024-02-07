""" PurrSong (Lavviebot) Component """
from __future__ import annotations

from lavviebot.exceptions import LavviebotAuthError

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_USERNAME, CONF_PASSWORD
from homeassistant.core import HomeAssistant

from .const import DOMAIN, LOGGER, PLATFORMS
from .coordinator import LavviebotDataUpdateCoordinator
from .util import NoDevicesError, async_validate_api

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PurrSong from a config entry."""

    coordinator = LavviebotDataUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload PurrSong config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        del hass.data[DOMAIN][entry.entry_id]
        if not hass.data[DOMAIN]:
            del hass.data[DOMAIN]
    return unload_ok

async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Migrate old entry."""
    # Also set PurrSong account user_id as config unique_id
    if entry.version in [1,2]:
        if entry.version == 1:
            email = entry.data[CONF_USERNAME]
            password = entry.data[CONF_PASSWORD]
        if entry.version ==2:
            email = entry.data[CONF_EMAIL]
            password = entry.data[CONF_PASSWORD]

        try:
            await async_validate_api(email, password)
        except (LavviebotAuthError, ConnectionError, NoDevicesError):
            return False

        entry.version = 3

        LOGGER.debug(f'Migrating PurrSong config entry unique id to {email}')
        hass.config_entries.async_update_entry(
            entry,
            title='PurrSong',
            data={
                CONF_EMAIL: email,
                CONF_PASSWORD: password,

            },
            unique_id=email
        )

    return True
