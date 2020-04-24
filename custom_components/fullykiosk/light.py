"""Fully Kiosk Browser light entity for controlling screen brightness & on/off."""
import logging

from homeassistant.components.light import ATTR_BRIGHTNESS, Light, SUPPORT_BRIGHTNESS
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, COORDINATOR, CONTROLLER

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser light."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    controller = hass.data[DOMAIN][config_entry.entry_id][CONTROLLER]

    async_add_entities([FullyLight(coordinator, controller)], False)


class FullyLight(Light):
    def __init__(self, coordinator, controller):
        self._name = f"{coordinator.data['deviceName']} Screen"
        self.coordinator = coordinator
        self.controller = controller
        self._unique_id = f"{coordinator.data['deviceID']}-screen"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self.coordinator.data["isScreenOn"]

    @property
    def brightness(self):
        return self.coordinator.data["screenBrightness"]

    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.data["deviceID"])},
            "name": self.coordinator.data["deviceName"],
            "manufacturer": self.coordinator.data["deviceManufacturer"],
            "model": self.coordinator.data["deviceModel"],
            "sw_version": self.coordinator.data["appVersionName"],
        }

    @property
    def unique_id(self):
        return self._unique_id

    def turn_on(self, **kwargs):
        self.controller.screenOn()
        brightness = kwargs.get(ATTR_BRIGHTNESS)
        if brightness == None:
            return
        if brightness != self._brightness:
            self.controller.setScreenBrightness(brightness)

    def turn_off(self, **kwargs):
        self.controller.screenOff()

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()
