"""Constants for the HDFury integration."""

from __future__ import annotations

DOMAIN: str = "hdfury"

CONF_HOST: str = "host"

DEFAULT_NAME: str = "HDFury"
DEFAULT_PORT: int = 80

OPTIONS: list[str] = [
    "HDMI 1",
    "HDMI 2",
    "HDMI 3",
    "HDMI 4",
]

OPTION_TO_INDEX: dict[str, int] = {
    "HDMI 1": 0,
    "HDMI 2": 1,
    "HDMI 3": 2,
    "HDMI 4": 3,
}
