"""HDFury HTTP API client."""

from __future__ import annotations

import asyncio

from aiohttp import ClientError
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession


class HdfuryApi: # pylint: disable=too-few-public-methods
    """HDFury API client."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Initialize the API client."""
        self._hass: HomeAssistant = hass
        self._host: str = host

    async def async_set_input(self, input_index: int) -> None:
        """Set the active input."""
        session = async_get_clientsession(self._hass)
        url: str = f"http://{self._host}/cmd?insel{input_index}"

        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                await response.read()
        except ClientError as err:
            raise HdfuryApiError(f"Request failed: {url}") from err
        except asyncio.TimeoutError as err:
            raise HdfuryApiError(f"Request timed out: {url}") from err


class HdfuryApiError(Exception): # pylint: disable=too-few-public-methods
    """API request error."""
