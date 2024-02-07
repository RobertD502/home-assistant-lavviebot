""" Update platform for PurrSong integration."""
from __future__ import annotations

from lavviebot.model import Cat, LavvieScanner, LavvieTag, LitterBox

from homeassistant.components.update import (
    UpdateDeviceClass,
    UpdateEntity,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import LavviebotDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """ Set Up PurrSong Update Entities. """

    coordinator: LavviebotDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    update_sensors = []
    # Litter Boxes
    for device_id, device_data in coordinator.data.litterboxes.items():
        update_sensors.append(FirmwareUpdate(coordinator, device_id))

    # LavvieScanner
    for device_id, device_data in coordinator.data.lavvie_scanners.items():
        update_sensors.append(ScannerFirmwareUpdate(coordinator, device_id))

    # LavvieTag
    for device_id, device_data in coordinator.data.lavvie_tags.items():
        update_sensors.append(TagFirmwareUpdate(coordinator, device_id))

    async_add_entities(update_sensors)


class FirmwareUpdate(CoordinatorEntity, UpdateEntity):
    """ Representation of Lavviebot Firmware Update Availability """

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

        return str(self.device_data.device_id) + '_firmware_update'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Firmware update"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """
        
        return True

    @property
    def installed_version(self) -> str:
        """ Return Currently Installed Firmware Version """

        return self.device_data.current_firmware

    @property
    def latest_version(self) -> str:
        """ Return Latest Firmware Version Available """

        return self.device_data.latest_firmware

    @property
    def device_class(self) -> UpdateDeviceClass:
        """ Return Firmware device class """

        return UpdateDeviceClass.FIRMWARE


class ScannerFirmwareUpdate(CoordinatorEntity, UpdateEntity):
    """ Representation of LavvieScanner Firmware Update Availability """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LavvieScanner:
        """ Handle coordinator LavvieScanner data """

        return self.coordinator.data.lavvie_scanners[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "LavvieScanner",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_scanner_firmware_update'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Firmware update"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """
        
        return True

    @property
    def installed_version(self) -> str:
        """ Return Currently Installed Firmware Version """

        return self.device_data.current_firmware

    @property
    def latest_version(self) -> str:
        """ Return Latest Firmware Version Available """

        return self.device_data.latest_firmware

    @property
    def device_class(self) -> UpdateDeviceClass:
        """ Return Firmware device class """

        return UpdateDeviceClass.FIRMWARE


class TagFirmwareUpdate(CoordinatorEntity, UpdateEntity):
    """ Representation of LavvieTag Firmware Update Availability """

    def __init__(self, coordinator, device_id):
        super().__init__(coordinator)
        self.device_id = device_id


    @property
    def device_data(self) -> LavvieTag:
        """ Handle coordinator LavvieTag data """

        return self.coordinator.data.lavvie_tags[self.device_id]

    @property
    def device_info(self) -> dict[str, Any]:
        """ Return device registry information for this entity. """

        return {
            "identifiers": {(DOMAIN, self.device_data.device_id), (DOMAIN, self.device_data.iot_code_tail)},
            "name": self.device_data.device_name,
            "manufacturer": "PurrSong",
            "model": "LavvieTag",
            "sw_version": self.device_data.current_firmware
        }

    @property
    def unique_id(self) -> str:
        """ Sets unique ID for this entity. """

        return str(self.device_data.device_id) + '_tag_firmware_update'

    @property
    def name(self) -> str:
        """ Return name of the entity """

        return "Firmware update"

    @property
    def has_entity_name(self) -> bool:
        """ Indicate that entity has name defined """
        
        return True

    @property
    def installed_version(self) -> str:
        """ Return Currently Installed Firmware Version """

        return self.device_data.current_firmware

    @property
    def latest_version(self) -> str:
        """ Return Latest Firmware Version Available """

        return self.device_data.latest_firmware

    @property
    def device_class(self) -> UpdateDeviceClass:
        """ Return Firmware device class """

        return UpdateDeviceClass.FIRMWARE
