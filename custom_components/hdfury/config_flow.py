"""Config flow for the HDFury integration."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_HOST, DEFAULT_NAME, DOMAIN


class HdfuryConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 1

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> None:
        """Get the options flow."""
        return

    def is_matching(self, other_flow: config_entries.ConfigFlow) -> bool:
        """Return True if flows match."""
        return False

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        """Handle the user step."""
        if user_input is not None:
            host: str = user_input[CONF_HOST].strip()
            name: str = user_input[CONF_NAME].strip()

            await self.async_set_unique_id(host.lower())
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=name,
                data={
                    CONF_HOST: host,
                    CONF_NAME: name,
                },
            )

        schema: vol.Schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
                vol.Required(CONF_HOST): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors={},
        )
