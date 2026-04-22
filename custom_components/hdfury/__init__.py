"""The HDFury integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_HOST, DOMAIN
from .coordinator import HdfuryDataUpdateCoordinator
from .hdfury import HdfuryApi

PLATFORMS: list[Platform] = [Platform.SELECT, Platform.BUTTON]


async def async_setup(_hass: HomeAssistant, _config: dict[str, Any]) -> bool:
    """Set up the integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a config entry."""
    api: HdfuryApi = HdfuryApi(hass, entry.data[CONF_HOST])
    coordinator: HdfuryDataUpdateCoordinator = HdfuryDataUpdateCoordinator(hass, api)

    await coordinator.async_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok: bool = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
