"""HDFury HTTP API client."""

from __future__ import annotations

import asyncio

from aiohttp import ClientError
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession


class HdfuryApi:  # pylint: disable=too-few-public-methods
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

    async def async_get_input(self) -> int:
        """Get the active TX0 input."""
        session = async_get_clientsession(self._hass)
        url: str = f"http://{self._host}/ssi/infopage.ssi"

        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                data: dict[str, str] = await response.json()
        except ClientError as err:
            raise HdfuryApiError(f"Request failed: {url}") from err
        except asyncio.TimeoutError as err:
            raise HdfuryApiError(f"Request timed out: {url}") from err
        except ValueError as err:
            raise HdfuryApiError(f"Invalid response: {url}") from err

        value: str | None = data.get("portseltx0")
        if value is None:
            raise HdfuryApiError("Missing portseltx0 in response")

        try:
            input_index: int = int(value)
        except ValueError as err:
            raise HdfuryApiError(f"Invalid portseltx0 value: {value}") from err

        if input_index not in (0, 1, 2, 3):
            raise HdfuryApiError(f"Unexpected portseltx0 value: {input_index}")

        return input_index


class HdfuryApiError(Exception):
    """API request error."""
