import datetime
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Union

from aimlsse_api.data.metar import MetarProperty


class GroundDataAccess(ABC):
    """Provides access to station data of the ground-measurements data-source"""

    @abstractmethod
    async def queryMetar(self, data:dict, datetime_from:datetime, datetime_to:datetime):
        """
        Query data for the specified stations in the interval [datetime_from, datetime_to],
        where the properties are extracted from the METARs.

        Groups of parameters in the data, where at least one has to be present are annoted by [x].
        x refers to the group-identifier.
        All non-group parameters have to be present.
        
        Parameters
        ----------
        data: `JSON / dict`
        -   stations: `List[str]` [target]
                A list containing all stations that the data should be queried for
        -   polygons: `List[str]` [target]
                A list of polygons in the form of a well-known text (wkt)
                that specify the area to search for stations
        -   properties: `List[MetarProperty]`
                The properties to extract from the METARs
        
        datetime_from: `datetime.datetime`
            The beginning of the interval to be queried
        datetime_to: `datetime.datetime`
            The end of the interval to be queried
        
        Returns
        -------
        `application/JSON`
            The METAR data that is queried from the data source for the given datetime-interval
            (station, datetime, ..requested properties..)
        """
        pass

    @abstractmethod
    async def queryMetadata(self, data:dict):
        """
        Query metadata for the specified stations in the interval [date_from, date_to]
        
        Groups of parameters in the data, where at least one has to be present are annoted by [x].
        x refers to the group-identifier.
        All non-group parameters have to be present.

        Parameters
        ----------
        data: `JSON / dict`
        -   stations: `List[str]` [target]
                A list containing all stations that the metadata should be queried for
        -   polygons: `List[str]` [target]
                A list of polygons in the form of a well-known text (wkt)
                that specify the area to search for stations
        
        Returns
        -------
        `application/JSON`
            The metadata for the given stations (latitude in [degrees], longitude in [degrees], elevation in [meters], ..)
        """
        pass