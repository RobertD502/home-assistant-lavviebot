""" Binary Sensor platform for PurrSong integration."""
from __future__ import annotations

from lavviebot.model import LitterBox, Cat

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LavviebotDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """ Set Up PurrSong Binary Sensor Entities. """

    coordinator: LavviebotDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    binary_sensors = []
    for device_id, device_data in coordinator.data.litterboxes.items():
        binary_sensors.append(StorageRefill(coordinator, device_id))
        binary_sensors.append(WasteFull(coordinator, device_id))

    async_add_entities(binary_sensors)


class StorageRefill(CoordinatorEntity, BinarySensorEntity):
    """ Representation of Lavviebot Storage Refill Alert """

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

        return str(self.device_data.device_id) + '_storage_refill_needed'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Storage refill needed"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def is_on(self) -> bool:
        """ Return True if litter storage is empty """

        if self.device_data.top_litter_status == 0:
            return True
        else:
            return False

    @property
    def icon(self) -> str:
        """Set icon based on storage level"""

        if self.device_data.top_litter_status == 0:
            return 'mdi:alert-octagram'
        else:
            return 'mdi:octagram-outline'

class WasteFull(CoordinatorEntity, BinarySensorEntity):
    """ Representation of Lavviebot Waste Level Alert """

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

        return str(self.device_data.device_id) + '_waste_emptying_needed'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Waste drawer full"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """

        return True

    @property
    def is_on(self) -> bool:
        """ Return True if waste bin is full """

        if self.device_data.waste_drawer_status == 0:
            return True
        else:
            return False

    @property
    def icon(self) -> str:
        """Set icon based on waste level"""

        if self.device_data.waste_drawer_status == 0:
            return 'mdi:alert-octagram'
        else:
            return 'mdi:octagram-outline'
