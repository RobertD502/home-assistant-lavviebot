""" Config Flow for Purrsong (Lavviebot) integration """

from __future__ import annotations
from collections.abc import Mapping
from typing import Any

from lavviebot.exceptions import LavviebotAuthError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DEFAULT_NAME, DOMAIN
from .util import NoLitterBoxesError, NoUserIdError, async_validate_api

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_EMAIL): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
    }
)

class LavviebotConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """ Handle a config flow for Purrsong integration """

    VERSION = 2

    entry: config_entries.ConfigEntry | None

    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> FlowResult:
        """ Handle re-authentication with Purrsong. """

        self.entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        return await self.async_step_reauth_confirm()

    async def async_step_reauth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm re-authentication with Purrsong."""
        
        errors: dict[str, str] = {}

        if user_input:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]
            try:
                user_id = await async_validate_api(self.hass, email, password)
            except LavviebotAuthError:
                errors["base"] = "invalid_auth"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except NoLitterBoxesError:
                errors["base"] = "no_litter_boxes"
            except NoUserIdError:
                errors["base"] = "no_user_id"
            else:
                assert self.entry is not None

                self.hass.config_entries.async_update_entry(
                    self.entry,
                    data={
                        **self.entry.data,
                        CONF_EMAIL: email,
                        CONF_PASSWORD: password,

                    },
                )
                await self.hass.config_entries.async_reload(self.entry.entry_id)
                return self.async_abort(reason="reauth_successful")
                errors["base"] = "incorrect_email_pass"

        return self.async_show_form(
            step_id="reauth_confirm",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input:

            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]
            try:
                user_id = await async_validate_api(self.hass, email, password)
            except LavviebotAuthError:
                errors["base"] = "invalid_auth"
            except ConnectionError:
                errors["base"] = "cannot_connect"
            except NoLitterBoxesError:
                errors["base"] = "no_litter_boxes"
            except NoUserIdError:
                errors["base"] = "no_user_id"
            else:
                await self.async_set_unique_id(user_id)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data={CONF_EMAIL: email, CONF_PASSWORD: password},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )
