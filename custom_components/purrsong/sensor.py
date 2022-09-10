""" Sensor platform for PurrSong integration."""
from __future__ import annotations

from typing import Any

from datetime import datetime
from lavviebot.model import LitterBox, Cat
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import(
    MASS_POUNDS,
    PERCENTAGE,
    TEMP_CELSIUS,
    TIME_MINUTES,
    TIME_SECONDS,
)

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LavviebotDataUpdateCoordinator


LITTER_TYPE = {
    0: 'Bentonite',
    1: 'Natural',
}

STORAGE_STATUS = {
    0: 'Refill Needed',
    1: 'Almost Empty',
    2: 'Full',
}

WASTE_STATUS = {
    0: 'Full',
    1: 'Almost Full',
    2: 'Empty or Piled',
}


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """ Set Up PurrSong Sensor Entities. """

    coordinator: LavviebotDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    """ Handle Cats first followed by Litter Boxes. """

    sensors = []
    for cat_id, cat_data in coordinator.data.cats.items():
        sensors.append(CatWeight(coordinator, cat_id))
        sensors.append(Duration(coordinator, cat_id))
        sensors.append(UseCount(coordinator, cat_id))

    for device_id, device_data in coordinator.data.litterboxes.items():
        sensors.append(Humidity(coordinator, device_id))
        sensors.append(Temperature(coordinator, device_id))
        sensors.append(BeaconBattery(coordinator, device_id))
        sensors.append(LastCatUsed(coordinator, device_id))
        sensors.append(LastSeen(coordinator, device_id))
        sensors.append(LastUsed(coordinator, device_id))
        sensors.append(LastUsedDuration(coordinator, device_id))
        sensors.append(LitterBottomAmnt(coordinator, device_id))
        sensors.append(LitterType(coordinator, device_id))
        sensors.append(MinBottomWeight(coordinator, device_id))
        sensors.append(TopLitterStatus(coordinator, device_id))
        sensors.append(WaitTime(coordinator, device_id))
        sensors.append(WasteStatus(coordinator, device_id))

    async_add_entities(sensors)


class CatWeight(CoordinatorEntity, SensorEntity):
    """ Representation of Cat's Weight """

    def __init__(self, coordinator, cat_id):
        super().__init__(coordinator)
        self.cat_id = cat_id


    @property
    def cat_data(self) -> Cat:
        """ Handle coordinator cat data """
        
        return self.coordinator.data.cats[self.cat_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.cat_data.cat_id)},
            "name": self.cat_data.cat_name,
            "manufacturer": "PurrSong",
            "model": "Cat",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.cat_data.cat_id) + '_weight'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Weight"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> float:
        """ Return weight of cat in pounds """

        return round(self.cat_data.cat_weight_pnds, 1)

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return pounds as the native unit """

        return MASS_POUNDS

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state_class """

        return SensorStateClass.MEASUREMENT

    @property
    def icon(self) -> str:
        return 'mdi:scale'

class Duration(CoordinatorEntity, SensorEntity):
    """ Representation of Cat's Daily Litter Box use Duration """

    def __init__(self, coordinator, cat_id):
        super().__init__(coordinator)
        self.cat_id = cat_id


    @property
    def cat_data(self) -> Cat:
        """ Handle coordinator cat data """

        return self.coordinator.data.cats[self.cat_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.cat_data.cat_id)},
            "name": self.cat_data.cat_name,
            "manufacturer": "PurrSong",
            "model": "Cat",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.cat_data.cat_id) + '_litter_box_duration'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Today's average use duration"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> float | int:
        """ Return today's total duration in seconds """

        return round(self.cat_data.duration, 1)

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return seconds as the native unit """

        return TIME_SECONDS

    @property
    def icon(self) -> str:
        return 'mdi:clock-outline'


class UseCount(CoordinatorEntity, SensorEntity):
    """ Representation of Cat's Daily Litter Box use Count """

    def __init__(self, coordinator, cat_id):
        super().__init__(coordinator)
        self.cat_id = cat_id


    @property
    def cat_data(self) -> Cat:
        """ Handle coordinator cat data """

        return self.coordinator.data.cats[self.cat_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.cat_data.cat_id)},
            "name": self.cat_data.cat_name,
            "manufacturer": "PurrSong",
            "model": "Cat",
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.cat_data.cat_id) + '_litter_box_use_count'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Litter box use count"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> int:
        """ Return today's total count """

        return self.cat_data.poop_count

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state_class """

        return SensorStateClass.TOTAL_INCREASING

    @property
    def icon(self) -> str:
        return 'mdi:numeric'


class Humidity(CoordinatorEntity, SensorEntity):
    """ Representation of Litter Box Humidity """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_humidity'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Humidity"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> int:
        """ Return current humidity """

        return self.device_data.humidity

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return percent as the native unit """

        return PERCENTAGE

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class """

        return SensorDeviceClass.HUMIDITY

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class """

        return SensorStateClass.MEASUREMENT


class Temperature(CoordinatorEntity, SensorEntity):
    """ Representation of Litter Box Temperature """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_temperature'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Temperature"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> int:
        """ Return current temperature in Celsius """

        return self.device_data.temperature_c

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return Celsius as the native unit """

        return TEMP_CELSIUS

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class """

        return SensorDeviceClass.TEMPERATURE

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class """

        return SensorStateClass.MEASUREMENT


class BeaconBattery(CoordinatorEntity, SensorEntity):
    """ Representation of Beacon Battery Level """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_beacon_battery'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Beacon battery"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> Any:
        """ Return current battery level """

        return self.device_data.beacon_battery

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class """

        return SensorDeviceClass.BATTERY

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class """

        return SensorStateClass.MEASUREMENT

    @property
    def entity_category(self) -> EntityCategory:
        """ Set category to diagnostic. """

        return EntityCategory.DIAGNOSTIC


class LastCatUsed(CoordinatorEntity, SensorEntity):
    """ Representation of last cat to have used the litter box """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_last_cat_used'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Last cat used"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> str:
        """ Return name of last cat to have used the litter box """

        return self.device_data.last_cat_used_name

    @property
    def icon(self) -> str:
        return 'mdi:cat'


class LastSeen(CoordinatorEntity, SensorEntity):
    """ Representation of last date/time litter box connected to PurrSong servers """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_last_seen'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Last seen"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> datetime:
        """ Returns date/time of the last time litter box connected to PurrSong servers """

        return self.device_data.last_seen

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class """

        return SensorDeviceClass.TIMESTAMP

    @property
    def entity_category(self) -> EntityCategory:
        """ Set category to diagnostic. """

        return EntityCategory.DIAGNOSTIC

    @property
    def icon(self) -> str:
        return 'mdi:web'


class LastUsed(CoordinatorEntity, SensorEntity):
    """ Representation of last date/time litter box was used by a cat """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_last_used'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Last used"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> datetime:
        """ Returns date/time of the last time litter box was used by a cat """

        return self.device_data.last_used

    @property
    def device_class(self) -> SensorDeviceClass:
        """ Return entity device class """

        return SensorDeviceClass.TIMESTAMP


class LastUsedDuration(CoordinatorEntity, SensorEntity):
    """ Representation of seconds litter box was used by most recent cat """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_last_used_duration'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Last used duration"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> float:
        """ Returns number of seconds last cat used the litter box """

        return round(self.device_data.last_used_duration, 1)

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return seconds as the native unit """

        return TIME_SECONDS

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class """

        return SensorStateClass.MEASUREMENT

    @property
    def icon(self) -> str:
        return 'mdi:clock-outline'


class LitterBottomAmnt(CoordinatorEntity, SensorEntity):
    """ Representation of current litter weight in tray """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_litter_bottom_amnt'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Litter bottom amount"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> float:
        """ Returns number of pounds of litter in the tray """

        return round(self.device_data.litter_bottom_amount_pnds, 1)

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return pounds as the native unit """

        return MASS_POUNDS

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class """

        return SensorStateClass.MEASUREMENT

    @property
    def icon(self) -> str:
        return 'mdi:scale'


class LitterType(CoordinatorEntity, SensorEntity):
    """ Representation of current litter type """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_litter_type'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Litter type"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> str:
        """ Returns litter type """

        return LITTER_TYPE.get(self.device_data.litter_type, 'Unknown')

    @property
    def entity_category(self) -> EntityCategory:
        """ Set category to diagnostic. """

        return EntityCategory.DIAGNOSTIC

    @property
    def icon(self) -> str:
        return 'mdi:tray'


class MinBottomWeight(CoordinatorEntity, SensorEntity):
    """ Representation of minimum bottom weight that is set up """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id

    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_min_bottom_weight'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Minimum bottom weight"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> float:
        """ Returns number of pounds minimum bottom weight is set to """

        return round(self.device_data.min_bottom_weight_pnds, 1)

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return pounds as the native unit """

        return MASS_POUNDS

    @property
    def state_class(self) -> SensorStateClass:
        """ Return the type of state class """

        return SensorStateClass.MEASUREMENT

    @property
    def entity_category(self) -> EntityCategory:
        """ Set category to diagnostic. """

        return EntityCategory.DIAGNOSTIC

    @property
    def icon(self) -> str:
        return 'mdi:scale'


class TopLitterStatus(CoordinatorEntity, SensorEntity):
    """ Representation of litter storage status """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_storage_status'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Storage status"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> str:
        """ Returns status of litter storage compartment """

        return STORAGE_STATUS.get(self.device_data.top_litter_status, 'Unknown')

    @property
    def icon(self) -> str:
        """Set icon based on storage level"""
        if self.device_data.top_litter_status == 2:
            return 'mdi:gauge-full'
        if self.device_data.top_litter_status == 1:
            return 'mdi:gauge'
        if self.device_data.top_litter_status == 0:
            return 'mdi:gauge-empty'


class WaitTime(CoordinatorEntity, SensorEntity):
    """ Representation of minutes litter box is set to wait before scooping """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_wait_time'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Wait time"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> int:
        """ Returns number of minutes litter box is set to wait before scooping """

        return self.device_data.wait_time

    @property
    def native_unit_of_measurement(self) -> str:
        """ Return minutes as the native unit """

        return TIME_MINUTES

    @property
    def entity_category(self) -> EntityCategory:
        """ Set category to diagnostic. """

        return EntityCategory.DIAGNOSTIC

    @property
    def icon(self) -> str:
        return 'mdi:clock-outline'


class WasteStatus(CoordinatorEntity, SensorEntity):
    """ Representation of litter box waste status """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LitterBox:
        """ Handle coordinator litter box data """

        return self.coordinator.data.litterboxes[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "Lavviebot S",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_waste_status'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Waste status"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def native_value(self) -> str:
        """ Returns status of litter storage compartment """

        return WASTE_STATUS.get(self.device_data.waste_drawer_status, 'Unknown')

    @property
    def icon(self) -> str:
        """Set icon based on storage level"""
        if self.device_data.waste_drawer_status == 2:
            return 'mdi:gauge-empty'
        if self.device_data.waste_drawer_status == 1:
            return 'mdi:gauge'
        if self.device_data.waste_drawer_status == 0:
            return 'mdi:gauge-full'

