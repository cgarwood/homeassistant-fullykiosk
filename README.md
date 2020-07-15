# Fully Kiosk Browser integration for Home Assistant

Provides support for controlling some common Fully Kiosk options through Home Assistant. Requires Remote Administration to be enabled in the Fully Kiosk Browser settings.

Currently Supports:
- Turning screen on/off and setting screen brightness
- Toggling Fully Kiosk screensaver on/off
- A variety of sensors (battery level, charging status, wifi status, and more)

Uses upstream library [python-fullykiosk](https://github.com/cgarwood/python-fullykiosk)