"""Select entity for the HDFury integration."""

from __future__ import annotations

from typing import Any

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, OPTION_TO_INDEX, OPTIONS
from .coordinator import HdfuryDataUpdateCoordinator
from .hdfury import HdfuryApiError

INDEX_TO_OPTION: dict[int, str] = {value: key for key, value in OPTION_TO_INDEX.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the select entity."""
    coordinator: HdfuryDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([HdfurySelect(entry, coordinator)])


class HdfurySelect(
    CoordinatorEntity[HdfuryDataUpdateCoordinator],
    RestoreEntity,
    SelectEntity,
):  # pylint: disable=abstract-method
    """HDFury input select."""

    _attr_has_entity_name: bool = True
    _attr_name: str = "Input"
    _attr_options: list[str] = OPTIONS

    def __init__(
        self,
        entry: ConfigEntry,
        coordinator: HdfuryDataUpdateCoordinator,
    ) -> None:
        """Initialize the entity."""
        super().__init__(coordinator)
        self._entry: ConfigEntry = entry
        self._attr_unique_id: str = f"{entry.unique_id}_input"
        self._attr_device_info: dict[str, Any] = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.data[CONF_NAME],
            "manufacturer": "HDFury",
            "model": "HDFury",
        }
        self._attr_current_option: str = OPTIONS[0]

    async def async_added_to_hass(self) -> None:
        """Restore state."""
        await super().async_added_to_hass()

        last_state = await self.async_get_last_state()
        if last_state and last_state.state in OPTIONS:
            self._attr_current_option = last_state.state

    @property
    def current_option(self) -> str | None:
        """Return the current option."""
        if self.coordinator.data in INDEX_TO_OPTION:
            return INDEX_TO_OPTION[self.coordinator.data]
        return self._attr_current_option

    async def async_select_option(self, option: str) -> None:
        """Set selected option."""
        input_index: int = OPTION_TO_INDEX[option]

        try:
            await self.coordinator.api.async_set_input(input_index)
        except HdfuryApiError as err:
            raise HomeAssistantError(str(err)) from err

        self._attr_current_option = option
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()
