# Fully Kiosk Browser integration for Home Assistant

Provides support for controlling some common Fully Kiosk options through Home Assistant. Requires Remote Administration to be enabled in the Fully Kiosk Browser settings.

Currently Supports:

- Light entity for turning screen on/off and setting screen brightness
- Switch entities for controlling screensaver, maintenance mode, and kiosk protection
- A variety of sensors (battery level, charging status, wifi status, and more)
- A media player entity for playing audio files on the device

The `media_player` entity has a few extra services that allow you to restart fully, reboot the device, launch an app, load custom URLs, and more. See `custom_components/fullykiosk/services.yaml` for documentation on the various services.

Uses upstream library [python-fullykiosk](https://github.com/cgarwood/python-fullykiosk)


<a href="https://www.buymeacoffee.com/cgarwood" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 41px !important;" ></a>