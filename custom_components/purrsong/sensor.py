"""Support for Lavviebot S Litterboxes."""

import logging
import voluptuous as vol
from homeassistant.helpers import config_validation as cv, entity_platform
from homeassistant.components.sensor import SensorEntity
from homeassistant.const import MASS_POUNDS


"""Attributes"""

ATTR_LITTER_MIN_WEIGHT = "litter_min_weight"
ATTR_LITTER_CURRENT_WEIGHT = "litter_current_weight"
ATTR_TOP_LITTER_STATUS = "top_litter_status"
ATTR_TOP_LITTER_WEIGHT = "top_litter_weight"
ATTR_LITTER_TYPE = "litter_type"
ATTR_WAIT_TIME = "wait_time"
ATTR_TEMPERATURE = "temperature"
ATTR_HUMIDITY = "humidity"
ATTR_SET_CAT_WEIGHT = "set_cat_weight"
ATTR_POOP_COUNT = "poop_count"
ATTR_DURATION = "duration"
from .const import (
    DOMAIN
)



_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Platform uses config entry setup."""
    pass


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Lavviebot devices and cats."""
    lavviebot = hass.data[DOMAIN]

    platform = entity_platform.current_platform.get()

    devices = []
    cats = []
    for device in lavviebot.devices():
        devices.append(LavviebotLitterBox(device))

    for cat in lavviebot.cats():
        cats.append(LavviebotCat(cat))
    async_add_entities(devices)
    async_add_entities(cats)


class LavviebotLitterBox(SensorEntity):
    """Representation of a Lavviebt Litterbox."""

    def __init__(self, device):
        self._device = device
        self._available = True

    @property
    def unique_id(self):
        """Return the ID of this Lavviebot."""
        return self._device.lavviebot_id

    @property
    def name(self):
        """Return the name of the litterbox if any."""
        return self._device.name

    @property
    def state(self):
        """Returns waste status"""
        if self._device.waste_status == 2:
            return "Empty or Piled"
        if self._device.waste_status == 1:
            return "Almost Full"
        if self._device.waste_status == 0:
            return "Full"
        return None

    @property
    def icon(self):
        """Set litterbox icon based on waste level"""
        if self._device.waste_status == 2:
            return 'mdi:gauge-empty'
        if self._device.waste_status == 1:
            return 'mdi:gauge'
        if self._device.waste_status == 0:
            return 'mdi:gauge-full'

    @property
    def litter_min_weight(self) -> int:
        if self._device.litter_type == 0:
            return round(float(self._device.min_bottom_ben_weight), 1)
        if self._device.litter_type == 1:
            return round(float(self._device.min_bottom_nat_weight), 1)

    @property
    def litter_current_weight(self) -> int:
        return round(float(self._device.litter_bottom_amount), 1)

    @property
    def top_litter_status(self):
        if self._device.top_litter_status == 2:
            return "Full"
        if self._device.top_litter_status == 1:
            return "Almost Empty"
        if self._device.top_litter_status == 0:
            return "Refill"
        return None

    @property
    def litter_type(self):
        if self._device.litter_type == 0:
            return "Bentonite"
        if self._device.litter_type == 1:
            return "Natural"
        return None

    @property
    def wait_time(self) -> int:
        return self._device.wait_time

    @property
    def temperature(self) -> int:
        return round(((float(self._device.temperature) * (9/5)) + 32), 1)

    @property
    def humidity(self) -> int:
        return self._device.humidity

    @property
    def available(self):
        """Return true if device is available."""
        return self._available

    @property
    def device_state_attributes(self) -> dict:
        """Return optional state attributes."""
        return {
            ATTR_LITTER_MIN_WEIGHT: self.litter_min_weight,
            ATTR_LITTER_CURRENT_WEIGHT: self.litter_current_weight,
            ATTR_TOP_LITTER_STATUS: self.top_litter_status,
            ATTR_LITTER_TYPE: self.litter_type,
            ATTR_WAIT_TIME: self.wait_time,
            ATTR_TEMPERATURE: self.temperature,
            ATTR_HUMIDITY: self.humidity,
        }

    def update(self):
        """Update automation state."""
        _LOGGER.info("Refreshing device state")
        self._device.refresh()

class LavviebotCat(SensorEntity):
    """Representation of a Lavviebot Cat."""

    def __init__(self, cat):
        self._cat = cat
        self._available = True

    @property
    def unique_id(self):
        """Return id of cat."""
        return self._cat.cat_id

    @property
    def name(self):
        """Return the name of the litterbox if any."""
        return self._cat.cat_name

    @property
    def state(self) -> int:
        """Return most recent cat weight"""
        if self._cat.cat_attributes['cat_weight_today'] == None:
            return 0
        return round(float(self._cat.cat_attributes['cat_weight_today']), 1)

    @property
    def icon(self):
        """Set cat sensor icons to cat"""
        return 'mdi:cat'

    @property
    def unit_of_measurement(self):
        return MASS_POUNDS

    @property
    def set_cat_weight(self) -> int:
        if self._cat.cat_attributes['cat_weight'] == None:
            return 0
        return round(float(self._cat.cat_attributes['cat_weight']), 1)

    @property
    def poop_count(self) -> int:
        if self._cat.cat_attributes['poop_count'] == None:
            return 0
        return self._cat.cat_attributes['poop_count']

    @property
    def duration(self) -> int:
        if self._cat.cat_attributes['duration'] == None:
            return 0
        return round(float(self._cat.cat_attributes['duration']), 1)

    @property
    def available(self):
        """Return true if device is available."""
        return self._available

    @property
    def device_state_attributes(self) -> dict:
        """Return optional state attributes."""
        return {
            ATTR_SET_CAT_WEIGHT: self.set_cat_weight,
            ATTR_POOP_COUNT: self.poop_count,
            ATTR_DURATION: self.duration,
        }

    def update(self):
        """Update automation state."""
        _LOGGER.info("Refreshing device state")
        self._cat.refresh()