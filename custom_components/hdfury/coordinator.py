"""Coordinator for the HDFury integration."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .hdfury import HdfuryApi, HdfuryApiError

_LOGGER = logging.getLogger(__name__)


class HdfuryDataUpdateCoordinator(DataUpdateCoordinator[int]):
    """Coordinate HDFury data updates."""

    def __init__(self, hass: HomeAssistant, api: HdfuryApi) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="HDFury",
            update_interval=timedelta(seconds=10),
        )
        self.api: HdfuryApi = api

    async def _async_update_data(self) -> int:
        """Fetch data from the device."""
        try:
            return await self.api.async_get_input()
        except HdfuryApiError as err:
            raise UpdateFailed(str(err)) from err
