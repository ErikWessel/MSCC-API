import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type, Union

class UnitEnum(str, Enum):
    pass

class UnitDistance(UnitEnum):
    STATUTE_MILES = 'SM'
    MILES = 'MI'
    METERS = 'M'
    KILOMETERS = 'KM'
    FEET = 'FT'
    INCHES = 'IN'

class UnitPrecipitation(UnitEnum):
    INCHES = 'IN'
    CENTIMETERS = 'CM'

class UnitPressure(UnitEnum):
    MILLIBAR = 'MB'
    HECTOPASCAL = 'HPA'
    INCHES = 'IN'

class UnitSpeed(UnitEnum):
    KNOTS = 'KT'
    METERS_PER_SECOND = 'MPS'
    KILOMETERS_PER_HOUR = 'KMH'
    MILES_PER_HOUR = 'MPH'

class UnitTemperature(UnitEnum):
    FAHRENHEIT = 'F'
    CELSIUS = 'C'
    KELVIN = 'K'

class MetarPropertyType(Enum):
    METAR_CODE                  = ('metar_code')
    REPORT_TYPE                 = ('report_type')
    REPORT_CORRECTION           = ('report_correction')
    REPORT_MODE                 = ('report_mode')
    STATION_ID                  = ('station_id')
    TIME                        = ('time')
    OBSERVATION_CYCLE           = ('observation_cycle')
    WIND_DIRECTION              = ('wind_direction [deg]')
    WIND_SPEED                  = ('wind_speed',                       UnitSpeed)
    WIND_GUST_SPEED             = ('wind_gust_speed',                  UnitSpeed)
    WIND_DIRECTION_FROM         = ('wind_direction_from [deg]')
    WIND_DIRECTION_TO           = ('wind_direction_to [deg]')
    VISIBILITY                  = ('visibility',                       UnitDistance)
    VISIBILITY_DIRECTION        = ('visibility_direction [deg]')
    MAX_VISIBILITY              = ('max_visibility',                   UnitDistance)
    MAX_VISIBILITY_DIRECTION    = ('max_visibility_direction [deg]')
    TEMPERATURE                 = ('temperature',                      UnitTemperature)
    DEW_POINT                   = ('dew_point',                        UnitTemperature)
    PRESSURE                    = ('pressure',                         UnitPressure)
    RUNWAY_VISIBILITY           = ('runway_visibility')
    CURRENT_WEATHER             = ('current_weather')
    RECENT_WEATHER              = ('recent_weather')
    SKY_CONDITIONS              = ('sky_conditions')
    RUNWAY_WINDSHEAR            = ('runway_windshear')
    WIND_SPEED_PEAK             = ('wind_speed_peak',                  UnitSpeed)
    WIND_DIRECTION_PEAK         = ('wind_direction_peak [deg]')
    PEAK_WIND_TIME              = ('peak_wind_time')
    WIND_SHIFT_TIME             = ('wind_shift_time')
    MAX_TEMPERATURE_6H          = ('max_temperature_6h',               UnitTemperature)
    MIN_TEMPERATURE_6H          = ('min_temperature_6h',               UnitTemperature)
    MAX_TEMPERATURE_24H         = ('max_temperature_24h',              UnitTemperature)
    MIN_TEMPERATURE_24H         = ('min_temperature_24h',              UnitTemperature)
    PRESSURE_AT_SEA_LEVEL       = ('pressure_at_sea_level',            UnitPressure)
    PRECIPITATION_1H            = ('precipitation_1h',                 UnitPrecipitation)
    PRECIPITATION_3H            = ('precipitation_3h',                 UnitPrecipitation)
    PRECIPITATION_6H            = ('precipitation_6h',                 UnitPrecipitation)
    PRECIPITATION_24H           = ('precipitation_24h',                UnitPrecipitation)
    SNOW_DEPTH                  = ('snow_depth',                       UnitDistance)
    ICE_ACCRETION_1H            = ('ice_accretion_1h',                 UnitDistance)
    ICE_ACCRETION_3H            = ('ice_accretion_3h',                 UnitDistance)
    ICE_ACCRETION_6H            = ('ice_accretion_6h',                 UnitDistance)

    def __init__(self, representation_name: str, unit_type: Type[Optional[UnitEnum]] = None):
        self.representation_name = representation_name
        self.unit_type = unit_type
    
    def get_representation_name(self) -> str:
        return self.representation_name
    
    def get_unit_type(self) -> Type[Optional[UnitEnum]]:
        return self.unit_type

class MetarProperty():
    type: MetarPropertyType
    unit: Optional[UnitEnum] = None

    def __init__(self, type:MetarPropertyType, unit:Optional[UnitEnum] = None) -> None:
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.type = type
        expected_type = type.get_unit_type()
        if unit is not None:
            if (expected_type is None) or (not isinstance(unit, type.get_unit_type())):
                raise ValueError(f'Property {type.name} may not be expressed in the unit {unit.name}, expected type {expected_type} for unit.')
            self.unit = unit
        else:
            if expected_type is None:
                self.unit = None
            else:
                # Change missing type to something appropriate
                if expected_type is UnitDistance:
                    self.unit = UnitDistance.METERS
                elif expected_type is UnitPrecipitation:
                    self.unit = UnitPrecipitation.CENTIMETERS
                elif expected_type is UnitPressure:
                    self.unit = UnitPressure.HECTOPASCAL
                elif expected_type is UnitSpeed:
                    self.unit = UnitSpeed.KILOMETERS_PER_HOUR
                elif expected_type is UnitTemperature:
                    self.unit = UnitTemperature.CELSIUS
                
                self.logger.warning(f'Property {type.name} was not supplied with a unit, eventhough {expected_type} was expected. '
                    f'Automatically set type to {self.unit.name}.')

    def __str__(self) -> str:
        repr_name = self.type.get_representation_name()
        if self.unit is None:
            return repr_name
        return f'{repr_name} [{self.unit.value}]'
    
    @staticmethod
    def from_string(specification:str):
        data_strings = specification.split(' ')
        unit = None
        logging.debug(f'Trying to create MetarProperty from: {data_strings}')
        type = MetarPropertyType[data_strings[0].upper()]
        expected_type = type.get_unit_type()
        if len(data_strings) == 2:
            unit = expected_type(data_strings[1][1:-1])
        return MetarProperty(type, unit)
