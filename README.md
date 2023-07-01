# This is now a Home Assistant core integration
This integration is now part of the Home Assistant core, and this repository is now archived. Documentation on the core integration are available at https://www.home-assistant.io/integrations/fully_kiosk/


# Fully Kiosk Browser integration for Home Assistant

Provides support for controlling some common Fully Kiosk options through Home Assistant. Requires Remote Administration to be enabled in the Fully Kiosk Browser settings.

Currently Supports:

- Light entity for turning screen on/off and setting screen brightness
- Switch entities for controlling screensaver, maintenance mode, and kiosk protection
- A variety of sensors (battery level, charging status, wifi status, and more)
- A few button entities for triggering functions on the tablet, such as restarting Fully, or reloading the start URL
- A media player entity for playing audio files on the device

The `media_player` entity has a few extra services that allow you to launch an app, load custom URLs, and more. See `custom_components/fullykiosk/services.yaml` for documentation on the various services.

Uses upstream library [python-fullykiosk](https://github.com/cgarwood/python-fullykiosk)

<a href="https://www.buymeacoffee.com/cgarwood" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/white_img.png" alt="Buy Me A Coffee"></a>

## Installation

The easiest way to install is through HACS. The Fully Kiosk Browser is already included in the HACS default repositories.

1. In Home Assistant, select HACS -> Integrations -> + Explore and Download Repositories. Search for Fully Kiosk Browser in the list and add it.
2. Restart Home Assistant
3. Set up and configure the integration: [![Add Integration](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=fullykiosk)

You will need your tablet's IP address and Fully's remote administration password to set up the integration.

## Manual Installation

Copy the `custom_components/fullykiosk` directory to your `custom_components` folder. Restart Home Assistant, and add the integration from the integrations page.
