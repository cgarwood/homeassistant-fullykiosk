"""Fully Kiosk Browser switch."""
import logging

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, COORDINATOR, CONTROLLER

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser switch."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    controller = hass.data[DOMAIN][config_entry.entry_id][CONTROLLER]

    async_add_entities([FullyScreenSaverSwitch(hass, coordinator, controller)], False)
    async_add_entities(
        [FullyMaintenanceModeSwitch(hass, coordinator, controller)], False
    )
    async_add_entities([FullyKioskLockSwitch(hass, coordinator, controller)], False)


class FullySwitch(SwitchEntity):
    """Representation of a generic Fully Kiosk Browser switch entity."""

    def __init__(self, hass, coordinator, controller):
        self.coordinator = coordinator
        self.controller = controller
        self.hass = hass

        self._name = ""
        self._unique_id = ""

    @property
    def name(self):
        return self._name

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

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()


class FullyScreenSaverSwitch(FullySwitch):
    """Representation of a Fully Kiosk Browser screensaver switch."""

    def __init__(self, hass, coordinator, controller):
        super().__init__(hass, coordinator, controller)
        self._name = f"{coordinator.data['deviceName']} Screensaver"
        self._unique_id = f"{coordinator.data['deviceID']}-screensaver"

    @property
    def is_on(self):
        if self.coordinator.data["appVersionCode"] < 784:
            return self.coordinator.data["currentFragment"] == "screensaver"
        return self.coordinator.data["isInScreensaver"]

    async def async_turn_on(self, **kwargs):
        await self.hass.async_add_executor_job(self.controller.startScreensaver)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs):
        await self.hass.async_add_executor_job(self.controller.stopScreensaver)
        await self.coordinator.async_refresh()


class FullyMaintenanceModeSwitch(FullySwitch):
    """Representation of a Fully Kiosk Browser maintenance mode switch."""

    def __init__(self, hass, coordinator, controller):
        super().__init__(hass, coordinator, controller)
        self._name = f"{coordinator.data['deviceName']} Maintenance Mode"
        self._unique_id = f"{coordinator.data['deviceID']}-maintenance"

    @property
    def is_on(self):
        return self.coordinator.data["maintenanceMode"]

    async def async_turn_on(self, **kwargs):
        await self.hass.async_add_executor_job(self.controller.enableLockedMode)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs):
        await self.hass.async_add_executor_job(self.controller.disableLockedMode)
        await self.coordinator.async_refresh()


class FullyKioskLockSwitch(FullySwitch):
    """Representation of a Fully Kiosk Browser kiosk lock switch."""

    def __init__(self, hass, coordinator, controller):
        super().__init__(hass, coordinator, controller)
        self._name = f"{coordinator.data['deviceName']} Kiosk Lock"
        self._unique_id = f"{coordinator.data['deviceID']}-kiosk"

    @property
    def is_on(self):
        return self.coordinator.data["kioskLocked"]

    async def async_turn_on(self, **kwargs):
        await self.hass.async_add_executor_job(self.controller.lockKiosk)
        await self.coordinator.async_refresh()

    async def async_turn_off(self, **kwargs):
        await self.hass.async_add_executor_job(self.controller.unlockKiosk)
        await self.coordinator.async_refresh()
