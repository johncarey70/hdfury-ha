"""HDFury HTTP API client."""

from __future__ import annotations

import asyncio
import json
from urllib.parse import quote

from aiohttp import ClientError

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession


class HdfuryApi:  # pylint: disable=too-few-public-methods
    """HDFury API client."""

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Initialize the API client."""
        self._hass: HomeAssistant = hass
        self._host: str = host

    async def _async_get(self, path: str) -> str:
        """Send a GET request and return the response text."""
        session = async_get_clientsession(self._hass)
        url: str = f"http://{self._host}{path}"

        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                return await response.text()
        except ClientError as err:
            raise HdfuryApiError(f"Request failed: {url} ({err})") from err
        except asyncio.exceptions.TimeoutError as err:
            raise HdfuryApiError(f"Request timed out: {url} ({err})") from err

    async def _async_send_command(self, command: str) -> None:
        """Send a raw command."""
        await self._async_get(f"/cmd?{quote(command, safe='=&')}")

    async def async_set_input(self, input_index: int) -> None:
        """Set the active input."""
        await self._async_send_command(f"insel{input_index}")

    async def async_reboot(self) -> None:
        """Reboot the device."""
        await self._async_send_command("reboot=")

    async def async_hotplug(self) -> None:
        """Issue hotplug."""
        await self._async_send_command("hotplug=")

    async def async_get_input(self) -> int:
        """Get the active TX0 input."""
        text: str = await self._async_get("/ssi/infopage.ssi")

        try:
            data: dict[str, str] = json.loads(text)
        except json.JSONDecodeError as err:
            raise HdfuryApiError(
                f"Invalid JSON response: /ssi/infopage.ssi ({err})"
            ) from err

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


class HdfuryApiError(Exception):  # pylint: disable=too-few-public-methods
    """API request error."""
