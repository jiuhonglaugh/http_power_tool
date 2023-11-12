# my_sensor/sensor.py
import logging
import requests
from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_HOST, CONF_PORT, CONF_SSL
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

DOMAIN = "http_power_tool"


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the custom integration."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the custom integration from a config entry."""
    host = entry.data.get(CONF_HOST)
    port = entry.data.get(CONF_PORT)
    use_ssl = entry.data.get(CONF_SSL)

    # 创建自定义实体
    hpt = HttpPowerTool(hass, host, port, use_ssl)
    # 添加实体到 Home Assistant
    hass.data[DOMAIN] = hpt
    hass.async_add_job(hpt.async_update_state)
    _LOGGER.info(f'Init {DOMAIN}: host {host}, port: {port}, use_ssl: {use_ssl} ')
    return True


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    async_add_entities([HttpPowerTool()])


class HttpPowerTool(Entity):
    def __init__(self, hass, host, port, use_ssl):
        self._host = host
        self._port = port
        self._use_ssl = use_ssl
        self._state = None

    # return entity name
    @property
    def name(self):
        return DOMAIN

    # return state
    @property
    def state(self):
        return self._state

    # Update the state of the entity.
    async def async_update_state(self, *_):
        url = f"http{'s' if self._use_ssl else ''}://{self._host}:{self._port}/state"
        try:
            response = requests.get(url)
            response.raise_for_status()
            self._state = response.text
            _LOGGER.info("Successfully updated state: %s", self._state)
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Error updating state: %s", str(e))
            self._state = None

        # Schedule the next update after a certain interval (e.g., every 60 seconds)
        await self.hass.helpers.event.async_call_later(60, self.async_update_state)

    async def async_open_device(self):
        """Open the device."""
        open_url = f"http{'s' if self._use_ssl else ''}://{self._host}:{self._port}/open"

        try:
            response = requests.get(open_url)
            response.raise_for_status()
            _LOGGER.info("Device opened successfully.")
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Error opening device: %s", str(e))

    async def async_close_device(self):
        """Close the device."""
        close_url = f"http{'s' if self._use_ssl else ''}://{self._host}:{self._port}/close"

        try:
            response = requests.get(close_url)
            response.raise_for_status()
            _LOGGER.info("Device closed successfully.")
        except requests.exceptions.RequestException as e:
            _LOGGER.error("Error closing device: %s", str(e))
