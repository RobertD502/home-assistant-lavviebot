# LavvieBot S [![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)  ![GitHub manifest version (path)](https://img.shields.io/github/manifest-json/v/RobertD502/home-assistant-lavviebot?filename=custom_components%2Fpurrsong%2Fmanifest.json) 
<a href="https://www.buymeacoffee.com/RobertD502" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="100" width="424"></a>
<a href="https://liberapay.com/RobertD502/donate"><img alt="Donate using Liberapay" src="https://liberapay.com/assets/widgets/donate.svg" height="100" width="300"></a>

### A lot of work has been put into creating the backend and this integration. If you enjoy this integration, consider donating by clicking on one of the supported methods above.


***All proceeds go towards helping a local animal rescue.**


### Custom component for Home Assistant for monitoring LavvieBot S litter boxes and associated cats

## Prior To Installation

You will need to create a new account in the PurrSong app and then share an invite from your primary account to the newly created account. If you use your primary account with this custom component, the primary account will get logged out off the app on your mobile device. This can be avoided by creating a dedicated account as previously mentioned.

## Installation

**Minimum Home Assistant version requirement:** `2022.11.0`

### With HACS
1. Open HACS Settings and add this repository (https://github.com/RobertD502/home-assistant-lavviebot)
as a Custom Repository (use **Integration** as the category).
2. The `LavvieBot S` page should automatically load (or find it in the HACS Store)
3. Click `Install`

### Manual
From this repo, copy the `purrsong` directory from `custom_components` and place it inside of your Home Assistant Core installation's `custom_components` directory.

`Note`: If installing manually, in order to be alerted about new releases, you will need to subscribe to releases from this repository. 

## Setup
1. Install this integration.
2. Navigate to the Home Assistant Integrations page (Settings --> Devices & Services)
3. Click the `+ ADD INTEGRATION` button in the lower right-hand corner
4. Search for `Lavviebot` or `PurrSong`

Alternatively, click on the button below to add the integration:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=purrsong)

## Features

Litter boxes and cats are exposed as devices along with their associated entities. See below for entities available.

##


### Litter Box

| Entity | Entity type | Description |
| --- | --- | --- |
| `Beacon battery` | `sensor` | Battery level for [LavvieBeacon Antenna Module](https://www.robotshop.com/en/lavviebeacon-antenna-module-lavvietag-lavviebot-s.html). State is `Unknown` if there is no LavvieBeacon associated with the litter box. |
| `Error time` | `sensor` | When the error, displayed in the `Latest error` sensor, occurred. |
| `Humidity` | `sensor` | Humidity as reported by the litter box. |
| `Last cat used` | `sensor` | Name of the last cat that used the litter box. Value will be "Unknown" if cat named "Unknown" used the litter box last. |
| `Last seen` | `sensor` | Displays date and time of the last time litter box communicated with PurrSong servers. |
| `Last used` | `sensor` | Displays date and time of the last time litter box was used by a cat. |
| `Last used duration` | `sensor` | Use duration of the cat that used the litter box last. Reported in seconds. |
| `Latest error` | `sensor` | Descriptive status of the last error in the litter box error logs. Possible states include: <ul><li>Auto-cleaning stopped. Please check if anything is blocking inside the litter tray.</li><li>Main motor overload occurred</li><li>Main motor or adapter error</li><li>Litter auto-refill stopped</li><li>Unknown error code</li> |
| `Litter bottom amount` | `sensor` | Weight of litter currently in the litter tray. |
| `Litter type` | `sensor` | Type of litter being used. Can be Bentonite or Natural. |
| `Minimum bottom weight` | `sensor` | Minimum weight that litter tray is set to have in it. |
| `Storage refill needed` | `binary_sensor` | `On` if fresh litter storage compartment is empty. Otherwise `Off`. Can be used to set up alerts. |
| `Storage status` | `sensor` | Descriptive status of the litter level in the fresh litter storage compartment. Possible states include: <ul><li>Refill Needed</li><li>Almost Empty</li><li>Full</li> |
| `Temperature` | `sensor` | Temperature as reported by the litter box. |
| `Use count` | `sensor` | Displays the total amount of times Lavviebot litter box was used today. |
| `Wait time` | `sensor` | Minutes litter box is set to wait, after it has been used, before scooping. |
| `Waste drawer full` | `binary_sensor` | `On` if the waste drawer is full. Otherwise `Off`. Can be used to set up alerts. |
| `Waste status` | `sensor` | Descriptive status of the waste level in the waste drawer. Possible states include: <ul><li>Full</li><li>Almost Full</li><li>Empty or Piled</li> |
| `Firmware update` | `update` | If Lavviebot has a firmware update available, the version of the new firmware will be shown. If Lavviebot firmware is up-to-date, "Up-to-date" will be shown. |


### Cat

| Entity | Entity type | Description |
| --- | --- | --- |
| `Litter box use count` | `sensor` | Total number of times cat has used the litter box today. |
| `Litter box use duration` | `sensor` | Total length of time cat has used the litter box today (in seconds). |
| `Weight` | `sensor` | Most recent cat weight obtained for the current day |


