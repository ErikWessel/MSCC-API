import logging
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

import numpy as np
import pandas as pd
from dacite import from_dict


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

UnitType = Optional[UnitEnum]

@dataclass
class DataRunwayVisibility:
    runway:         Optional[str]
    lowest_value:   Optional[float]
    highest_value:  Optional[float]

@dataclass
class DataWeather:
    intensity:      Optional[str]
    description:    Optional[str]
    precipitation:  Optional[str]
    obscuration:    Optional[str]
    other:          Optional[str]

@dataclass
class DataSkyConditions:
    cover:  Optional[str]
    height: Optional[float]
    cloud:  Optional[str]

class MetarPropertyType(Enum):
    METAR_CODE                  = ('metar_code',                str)
    REPORT_TYPE                 = ('report_type',               str)
    REPORT_CORRECTION           = ('report_correction',         Optional[str])
    REPORT_MODE                 = ('report_mode',               str)
    STATION_ID                  = ('station_id',                str)
    TIME                        = ('time',                      np.datetime64)
    OBSERVATION_CYCLE           = ('observation_cycle',         int)
    WIND_DIRECTION              = ('wind_direction',            float)
    WIND_SPEED                  = ('wind_speed',                float,                  UnitSpeed)
    WIND_GUST_SPEED             = ('wind_gust_speed',           float,                  UnitSpeed)
    WIND_DIRECTION_FROM         = ('wind_direction_from',       float)
    WIND_DIRECTION_TO           = ('wind_direction_to',         float)
    VISIBILITY                  = ('visibility',                float,                  UnitDistance)
    VISIBILITY_DIRECTION        = ('visibility_direction',      float)
    MAX_VISIBILITY              = ('max_visibility',            float,                  UnitDistance)
    MAX_VISIBILITY_DIRECTION    = ('max_visibility_direction',  float)
    TEMPERATURE                 = ('temperature',               float,                  UnitTemperature)
    DEW_POINT                   = ('dew_point',                 float,                  UnitTemperature)
    PRESSURE                    = ('pressure',                  float,                  UnitPressure)
    RUNWAY_VISIBILITY           = ('runway_visibility',         DataRunwayVisibility,   UnitDistance,   True,   True)
    CURRENT_WEATHER             = ('current_weather',           DataWeather,            None,           True,   True)
    RECENT_WEATHER              = ('recent_weather',            DataWeather,            None,           True,   True)
    SKY_CONDITIONS              = ('sky_conditions',            DataSkyConditions,      UnitDistance,   True,   True)
    RUNWAY_WINDSHEAR            = ('runway_windshear',          List[str],              None,           True,   False)
    WIND_SPEED_PEAK             = ('wind_speed_peak',           float,                  UnitSpeed)
    WIND_DIRECTION_PEAK         = ('wind_direction_peak',       float)
    PEAK_WIND_TIME              = ('peak_wind_time',            np.datetime64)
    WIND_SHIFT_TIME             = ('wind_shift_time',           np.datetime64)
    MAX_TEMPERATURE_6H          = ('max_temperature_6h',        float,                  UnitTemperature)
    MIN_TEMPERATURE_6H          = ('min_temperature_6h',        float,                  UnitTemperature)
    MAX_TEMPERATURE_24H         = ('max_temperature_24h',       float,                  UnitTemperature)
    MIN_TEMPERATURE_24H         = ('min_temperature_24h',       float,                  UnitTemperature)
    PRESSURE_AT_SEA_LEVEL       = ('pressure_at_sea_level',     float,                  UnitPressure)
    PRECIPITATION_1H            = ('precipitation_1h',          float,                  UnitPrecipitation)
    PRECIPITATION_3H            = ('precipitation_3h',          float,                  UnitPrecipitation)
    PRECIPITATION_6H            = ('precipitation_6h',          float,                  UnitPrecipitation)
    PRECIPITATION_24H           = ('precipitation_24h',         float,                  UnitPrecipitation)
    SNOW_DEPTH                  = ('snow_depth',                float,                  UnitDistance)
    ICE_ACCRETION_1H            = ('ice_accretion_1h',          float,                  UnitDistance)
    ICE_ACCRETION_3H            = ('ice_accretion_3h',          float,                  UnitDistance)
    ICE_ACCRETION_6H            = ('ice_accretion_6h',          float,                  UnitDistance)

    def __init__(self, representation_name: str, value_type, unit_type: UnitType = None,
        multi_value:bool = False, multi_entry:bool = False):
        self.representation_name = representation_name
        self.value_type = value_type
        self.unit_type = unit_type
        self.multi_value = multi_value
        self.multi_entry = multi_entry
    
    def get_representation_name(self) -> str:
        return self.representation_name
    
    def get_value_type(self):
        return self.value_type

    def get_unit_type(self) -> UnitType:
        return self.unit_type
    
    def uses_multiple_values(self) -> bool:
        return self.multi_value
    
    def has_multiple_entries(self) -> bool:
        return self.multi_entry

    @staticmethod
    def get_values_with_dataclass():
        return [
            MetarPropertyType.RUNWAY_VISIBILITY,
            MetarPropertyType.CURRENT_WEATHER,
            MetarPropertyType.RECENT_WEATHER,
            MetarPropertyType.SKY_CONDITIONS
        ]

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

class MetarPandas:

    @staticmethod
    def format_dataframe(data:pd.DataFrame, properties:List[MetarProperty]):
        data = data.infer_objects()
        types_with_dataclass = MetarPropertyType.get_values_with_dataclass()
        retyping_dict = {}
        for prop in properties:
            column_name = str(prop)
            if prop.type in types_with_dataclass:
                # Build dataclass from dict
                dataclass_type = prop.type.get_value_type()
                data[column_name] = data[column_name].apply(lambda x: [from_dict(dataclass_type, entry) for entry in x])
            elif prop.type != MetarPropertyType.RUNWAY_WINDSHEAR:
                # Specify type of column
                retyping_dict[column_name] = prop.type.get_value_type()
        data = data.astype(retyping_dict)
        return data
