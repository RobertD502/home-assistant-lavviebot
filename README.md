# LavvieBot S
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs) [![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/RobertD502/home-assistant-lavviebot.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/RobertD502/home-assistant-lavviebot/context:python) ![GitHub manifest version (path)](https://img.shields.io/github/manifest-json/v/RobertD502/home-assistant-lavviebot?filename=custom_components%2Fpurrsong%2Fmanifest.json) ![GitHub all releases](https://img.shields.io/github/downloads/RobertD502/home-assistant-lavviebot/total?color=green)

Custom component for Home Assistant Core for monitoring LavvieBot S Litterboxes and associated Cats

**Prior To Installation**

You will need to create a new account in the Purrsong app and then share an invite from your primary account to the newly created account. If you use your primary account with this custom component, the primary account will get logged out on your mobile device. This can be avoided by creating a dedicated account as previously mentioned.

## Installation

### With HACS
1. Open HACS Settings and add this repository (https://github.com/RobertD502/home-assistant-lavviebot)
as a Custom Repository (use **Integration** as the category).
2. The `LavvieBot S` page should automatically load (or find it in the HACS Store)
3. Click `Install`

### Manual
Copy the `purrsong` directory from `custom_components` in this repository,
and place inside your Home Assistant Core installation's `custom_components` directory.


## Setup
1. Install this integration.
2. Use Config Flow to configure the integration with your Purrsong credentials.
    * Initiate Config Flow by navigating to Configuration > Integrations > click the "+" button > find "LavvieBot S" (restart Home Assistant and / or clear browser cache if you can't find it)

## Features

### Litterbox Sensor
Litterbox sensors have a `state` that displays `waste level`. The litterbox sensor icon changes with `waste level`. The possible values are `Empty or Piled`, `Almost Full`, and `Full`

Available attributes:

| Attribute | Description |
| --- | --- |
| `status` | This attribute lets you know if there are any errors. Currently supported errors are `Auto Cleaning Stopped - Unknown Substances` and `Motor Overload` |
| `litter_min_weight` | This is the minimum weight of litter needed and is automatically set by your litterbox. Values differ between Natural litter and Bentonite litter. Unit of measurement is `lb`. |
| `litter_current_weight` | The amount of litter currently in your litterbox. Unit of measurement is `lb`. |
| `top_litter_status` | Keeps track of the fresh litter available. If sufficient fresh litter is available, displays `Full`. If fresh litter is present, but the storage light is off on the litterbox, attribute is set to `Almost Empty`. If no fresh litter is available then `Refill` is displayed. |
| `litter_type` | Displays the type of litter set from the litterbox (Natural or Bentonite). |
| `wait_time` | Displays the amount of time before litterbox will scoop waste. Time is in minutes. |
| `temperature` | Displays temperature reading from litterbox. Unit of measurement is `Fahrenheit`. |
| `humidity` | Displays humidity reading from litterbox. |

### Cat Sensor
Cat sensors have a `state` that displays the most recent `cat weight`. Unit of measurement should correspond to your Home Assistant settings.

Available attributes:

| Attribute | Description |
| --- | --- |
| `set_cat_weight` | This is the weight set for each cat from within the Purrsong app. |
| `poop_count` | The poop count for the current day. |
| `duration` | The average litterbox usage for the current day. Unit of measurement is `seconds` |
