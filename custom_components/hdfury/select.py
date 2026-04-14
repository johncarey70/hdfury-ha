"""Select entity for the HDFury integration."""

from __future__ import annotations

from datetime import timedelta
from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import CONF_HOST, DOMAIN, OPTION_TO_INDEX, OPTIONS
from .hdfury import HdfuryApi, HdfuryApiError

SCAN_INTERVAL = timedelta(seconds=10)

INDEX_TO_OPTION: dict[int, str] = {value: key for key, value in OPTION_TO_INDEX.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the select entity."""
    api: HdfuryApi = HdfuryApi(hass, entry.data[CONF_HOST])
    async_add_entities([HdfurySelect(entry, api)])


class HdfurySelect(RestoreEntity, SelectEntity):  # pylint: disable=abstract-method
    """HDFury input select."""

    _attr_has_entity_name: bool = True
    _attr_name: str = "Input"
    _attr_options: list[str] = OPTIONS

    def __init__(self, entry: ConfigEntry, api: HdfuryApi) -> None:
        """Initialize the entity."""
        self._entry: ConfigEntry = entry
        self._api: HdfuryApi = api
        self._attr_unique_id: str = f"{entry.unique_id}_input"
        self._attr_device_info: dict[str, Any] = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "HDFury",
            "model": "HDFury",
        }
        self._attr_current_option: str = OPTIONS[0]
        self._attr_available: bool = True

    async def async_added_to_hass(self) -> None:
        """Restore state."""
        await super().async_added_to_hass()

        last_state = await self.async_get_last_state()
        if last_state and last_state.state in OPTIONS:
            self._attr_current_option = last_state.state

        await self.async_update()

    async def async_update(self) -> None:
        """Update state from the device."""
        try:
            input_index: int = await self._api.async_get_input()
        except HdfuryApiError:
            self._attr_available = False
            return

        self._attr_current_option = INDEX_TO_OPTION[input_index]
        self._attr_available = True

    async def async_select_option(self, option: str) -> None:
        """Set selected option."""
        input_index: int = OPTION_TO_INDEX[option]

        try:
            await self._api.async_set_input(input_index)
        except HdfuryApiError as err:
            self._attr_available = False
            self.async_write_ha_state()
            raise HomeAssistantError(str(err)) from err

        self._attr_current_option = option
        self._attr_available = True
        self.async_write_ha_state()
