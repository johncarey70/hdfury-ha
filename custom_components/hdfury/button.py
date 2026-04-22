"""Button entities for the HDFury integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import CONF_HOST, DOMAIN
from .hdfury import HdfuryApi, HdfuryApiError


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up button entities."""
    api: HdfuryApi = HdfuryApi(hass, entry.data[CONF_HOST])
    async_add_entities(
        [
            HdfuryRebootButton(entry, api),
            HdfuryHotplugButton(entry, api),
        ]
    )


class HdfuryBaseButton(ButtonEntity):
    """Base HDFury button."""

    _attr_has_entity_name: bool = True

    def __init__(self, entry: ConfigEntry, api: HdfuryApi) -> None:
        """Initialize the button."""
        self._entry: ConfigEntry = entry
        self._api: HdfuryApi = api
        self._attr_device_info: dict[str, Any] = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "HDFury",
            "model": "HDFury",
        }


class HdfuryRebootButton(HdfuryBaseButton):
    """HDFury reboot button."""

    _attr_name: str = "Reboot"

    def __init__(self, entry: ConfigEntry, api: HdfuryApi) -> None:
        """Initialize the button."""
        super().__init__(entry, api)
        self._attr_unique_id: str = f"{entry.unique_id}_reboot"

    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            await self._api.async_reboot()
        except HdfuryApiError as err:
            raise HomeAssistantError(str(err)) from err


class HdfuryHotplugButton(HdfuryBaseButton):
    """HDFury hotplug button."""

    _attr_name: str = "Hotplug"

    def __init__(self, entry: ConfigEntry, api: HdfuryApi) -> None:
        """Initialize the button."""
        super().__init__(entry, api)
        self._attr_unique_id: str = f"{entry.unique_id}_hotplug"

    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            await self._api.async_hotplug()
        except HdfuryApiError as err:
            raise HomeAssistantError(str(err)) from err
