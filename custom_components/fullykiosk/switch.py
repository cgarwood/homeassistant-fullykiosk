"""Fully Kiosk Browser switch."""
import logging

from homeassistant.components.switch import SwitchDevice
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, COORDINATOR, CONTROLLER

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser switch."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    controller = hass.data[DOMAIN][config_entry.entry_id][CONTROLLER]
    switches = []

    device_info = {
        "identifiers": {(DOMAIN, coordinator.data["deviceID"])},
        "name": coordinator.data["deviceName"],
        "manufacturer": coordinator.data["deviceManufacturer"],
        "model": coordinator.data["deviceModel"],
        "sw_version": coordinator.data["appVersionName"],
    }

    async_add_entities(
        [FullyScreenSaverSwitch(coordinator, controller, device_info)], False
    )


class FullyScreenSaverSwitch(SwitchDevice):
    def __init__(self, coordinator, controller, device_info):
        self._name = f"{coordinator.data['deviceName']} Screensaver"
        self._device_info = device_info
        self.coordinator = coordinator
        self.controller = controller
        self._unique_id = f"{coordinator.data['deviceID']}-screensaver"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self.coordinator.data["currentFragment"] == "screensaver"

    @property
    def device_info(self):
        return self._device_info

    @property
    def unique_id(self):
        return self._unique_id

    def turn_on(self):
        self.controller.startScreensaver()

    def turn_off(self):
        self.controller.stopScreensaver()

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()
