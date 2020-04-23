"""Fully Kiosk Browser sensor."""
import logging

from homeassistant.components.binary_sensor import BinarySensorDevice
from homeassistant.const import DEVICE_CLASS_BATTERY
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import DOMAIN, COORDINATOR, CONTROLLER

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    "kioskMode": "Kiosk Mode",
    "kioskLocked": "Kiosk Locked",
    "plugged": "Pluggin In",
    "isDeviceAdmin": "Device Admin",
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser sensor."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]

    sensors = []

    device_info = {
        "identifiers": {(DOMAIN, coordinator.data["deviceID"])},
        "name": coordinator.data["deviceName"],
        "manufacturer": coordinator.data["deviceManufacturer"],
        "model": coordinator.data["deviceModel"],
        "sw_version": coordinator.data["appVersionName"],
    }

    for sensor in SENSOR_TYPES:
        sensors.append(FullyBinarySensor(coordinator, sensor, device_info))

    async_add_entities(sensors, False)


class FullyBinarySensor(BinarySensorDevice):
    def __init__(self, coordinator, sensor, device_info):
        self._name = f"{coordinator.data['deviceName']} {SENSOR_TYPES[sensor]}"
        self._device_info = device_info
        self._sensor = sensor
        self.coordinator = coordinator
        self._unique_id = f"{coordinator.data['deviceID']}-{sensor}"

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self.coordinator.data[self._sensor]

    @property
    def device_class(self):
        if self._sensor == "batteryLevel":
            return DEVICE_CLASS_BATTERY
        return None

    @property
    def device_info(self):
        return self._device_info

    @property
    def unique_id(self):
        return self._unique_id

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()
