"""Fully Kiosk Browser media_player entity."""
import logging
import voluptuous as vol

from homeassistant.helpers import config_validation as cv, entity_platform, service

from homeassistant.components.media_player import (
    ATTR_MEDIA_VOLUME_LEVEL,
    SERVICE_VOLUME_SET,
    SUPPORT_PLAY_MEDIA,
    SUPPORT_VOLUME_SET,
    MediaPlayerEntity,
)

SUPPORT_FULLYKIOSK = SUPPORT_PLAY_MEDIA | SUPPORT_VOLUME_SET

from .const import (
    DOMAIN, 
    COORDINATOR, 
    CONTROLLER,
    ATTR_STREAM,
    AUDIOMANAGER_STREAM_MUSIC
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser media player."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    controller = hass.data[DOMAIN][config_entry.entry_id][CONTROLLER]

    platform = entity_platform.current_platform.get()

    # This will call Entity.set_fullykiosk_volume_level(volume_level=VALUE, stream=VALUE)
    platform.async_register_entity_service(
        SERVICE_VOLUME_SET,
        {
            vol.Required(ATTR_MEDIA_VOLUME_LEVEL): cv.small_float,
            vol.Required(ATTR_STREAM): vol.All(
                vol.Number(scale=0),
                vol.Range(1, 10),
            ),
        },
        "async_set_fullykiosk_volume_level",
    )

    async_add_entities([FullyMediaPlayer(coordinator, controller)], False)


class FullyMediaPlayer(MediaPlayerEntity):
    """Representation of a Fully Kiosk Browser media player."""

    def __init__(self, coordinator, controller):
        self._name = f"{coordinator.data['deviceName']} Media Player"
        self.coordinator = coordinator
        self.controller = controller
        self._unique_id = f"{coordinator.data['deviceID']}-mediaplayer"

    @property
    def name(self):
        return self._name

    @property
    def supported_features(self):
        return SUPPORT_FULLYKIOSK

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

    def play_media(self, media_type, media_id, **kwargs):
        self.controller.playSound(media_id)

    def set_fullykiosk_volume_level(self, volume_level, stream):
        """Set volume level for a stream, range 0..1."""
        self.controller.sendCommand(
            cmd="setAudioVolume", level=str(int(volume_level * 100)), stream=str(stream)
        )

    async def async_set_fullykiosk_volume_level(self, volume_level, stream):
        """Set volume level for a stream, range 0..1."""
        await self.hass.async_add_executor_job(
            self.set_fullykiosk_volume_level, volume_level, stream
        )

    def set_volume_level(self, volume_level):
        """Set volume level, range 0..1."""
        self.set_fullykiosk_volume_level(volume_level=volume_level, stream=AUDIOMANAGER_STREAM_MUSIC)

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()
