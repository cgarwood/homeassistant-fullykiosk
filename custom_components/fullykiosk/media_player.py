"""Fully Kiosk Browser media_player entity."""
import logging

import voluptuous as vol
from homeassistant.components.media_player import (
    ATTR_MEDIA_VOLUME_LEVEL,
    SERVICE_VOLUME_SET,
    SUPPORT_PLAY_MEDIA,
    SUPPORT_VOLUME_SET,
    MediaPlayerEntity,
)
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_platform

from .const import (
    ATTR_APPLICATION,
    ATTR_CONFIG_TYPE,
    ATTR_KEY,
    ATTR_STREAM,
    ATTR_URL,
    ATTR_VALUE,
    AUDIOMANAGER_STREAM_MUSIC,
    CONTROLLER,
    COORDINATOR,
    DOMAIN,
    SERVICE_LOAD_START_URL,
    SERVICE_LOAD_URL,
    SERVICE_PLAY_AUDIO,
    SERVICE_RESTART_APP,
    SERVICE_SET_CONFIG,
    SERVICE_START_APPLICATION,
    SERVICE_TO_FOREGROUND,
)

SUPPORT_FULLYKIOSK = SUPPORT_PLAY_MEDIA | SUPPORT_VOLUME_SET


_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Fully Kiosk Browser media player."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id][COORDINATOR]
    controller = hass.data[DOMAIN][config_entry.entry_id][CONTROLLER]

    platform = entity_platform.current_platform.get()

    platform.async_register_entity_service(
        SERVICE_LOAD_START_URL, {}, "async_fullykiosk_load_start_url"
    )

    platform.async_register_entity_service(
        SERVICE_LOAD_URL, {vol.Required(ATTR_URL): cv.url}, "async_fullykiosk_load_url"
    )

    platform.async_register_entity_service(
        SERVICE_PLAY_AUDIO,
        {
            vol.Required(ATTR_URL): cv.string,
            vol.Required(ATTR_STREAM): vol.All(vol.Number(scale=0), vol.Range(1, 10)),
        },
        "async_fullykiosk_play_audio",
    )

    platform.async_register_entity_service(
        SERVICE_RESTART_APP, {}, "async_fullykiosk_restart"
    )

    platform.async_register_entity_service(
        SERVICE_SET_CONFIG,
        {
            vol.Required(ATTR_CONFIG_TYPE): vol.In(["string", "bool"]),
            vol.Required(ATTR_KEY): cv.string,
            vol.Required(ATTR_VALUE): vol.Any(cv.string, cv.boolean),
        },
        "async_fullykiosk_set_config",
    )

    platform.async_register_entity_service(
        SERVICE_VOLUME_SET,
        {
            vol.Required(ATTR_MEDIA_VOLUME_LEVEL): cv.small_float,
            vol.Required(ATTR_STREAM): vol.All(vol.Number(scale=0), vol.Range(1, 10)),
        },
        "async_fullykiosk_set_volume_level",
    )

    platform.async_register_entity_service(
        SERVICE_START_APPLICATION,
        {vol.Required(ATTR_APPLICATION): cv.string},
        "async_fullykiosk_start_app",
    )

    platform.async_register_entity_service(
        SERVICE_TO_FOREGROUND, {}, "async_fullykiosk_to_foreground"
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

    def fullykiosk_set_volume_level(self, volume_level, stream):
        """Set volume level for a stream, range 0..1."""
        self.controller.setAudioVolume(int(volume_level * 100), stream)

    def fullykiosk_play_audio(self, url, stream):
        """Play a piece of audio on a specific stream."""
        self.controller.playSound(url, stream)

    def play_media(self, media_type, media_id, **kwargs):
        """Play a piece of media."""
        self.fullykiosk_play_audio(media_id, AUDIOMANAGER_STREAM_MUSIC)

    def set_volume_level(self, volume_level):
        """Set volume level, range 0..1."""
        self.fullykiosk_set_volume_level(volume_level, AUDIOMANAGER_STREAM_MUSIC)

    async def async_fullykiosk_load_start_url(self):
        """Load the start URL on a fullykiosk browser."""
        await self.hass.async_add_executor_job(self.controller.loadStartUrl)

    async def async_fullykiosk_load_url(self, url):
        """Load URL on a fullykiosk browser."""
        await self.hass.async_add_executor_job(self.controller.loadUrl, url)

    async def async_fullykiosk_play_audio(self, url, stream):
        """Play a piece of audio on a specific stream."""
        await self.hass.async_add_executor_job(self.fullykiosk_play_audio, url, stream)

    async def async_fullykiosk_restart(self):
        """Restart the fullykiosk browser app."""
        await self.hass.async_add_executor_job(self.controller.restartApp)

    async def async_fullykiosk_set_config(self, config_type, key, value):
        """Set fullykiosk configuration value."""
        if config_type == "string":
            await self.hass.async_add_executor_job(
                self.controller.setConfigurationString, key, value
            )
        elif config_type == "bool":
            await self.hass.async_add_executor_job(
                self.controller.setConfigurationBool, key, value
            )

    async def async_fullykiosk_set_volume_level(self, volume_level, stream):
        """Set volume level for a stream, range 0..1."""
        await self.hass.async_add_executor_job(
            self.fullykiosk_set_volume_level, volume_level, stream
        )

    async def async_fullykiosk_start_app(self, application):
        """Start an application on the device running the fullykiosk browser app."""
        await self.hass.async_add_executor_job(
            self.controller.startApplication, application
        )

    async def async_fullykiosk_to_foreground(self):
        """Bring the fullykiosk browser app back to the foreground."""
        await self.hass.async_add_executor_job(self.controller.toForeground)

    async def async_added_to_hass(self):
        """Connect to dispatcher listening for entity data notifications."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )

    async def async_update(self):
        """Update Fully Kiosk Browser entity."""
        await self.coordinator.async_request_refresh()
