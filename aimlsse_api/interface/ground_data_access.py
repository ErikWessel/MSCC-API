import datetime
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Union

from aimlsse_api.data.metar import MetarProperty


class GroundDataAccess(ABC):
    """Provides access to station data of the ground-measurements data-source"""

    @abstractmethod
    async def queryMetar(self, data:dict, date_from:date, date_to:date):
        """
        Query data for the specified stations in the interval [date_from, date_to],
        where the properties are extracted from the METARs.
        
        Parameters
        ----------
        data: `JSON / dict`
        -   stations: `List[str]`
                A list containing all stations that the data should be queried for
        -   properties: `List[MetarProperty]`
                The properties to extract from the METARs
        
        date_from: `datetime.date`
            The beginning of the interval to be queried
        date_to: `datetime.date`
            The end of the interval to be queried
        
        Returns
        -------
        `application/JSON`
            The METAR data that is queried from the data source for the given date-interval
            (station, datetime, ..requested properties..)
        """
        pass

    @abstractmethod
    async def queryPosition(self, stations:List[str]):
        """
        Query data for the specified stations in the interval [date_from, date_to]
        
        Parameters
        ----------
        stations: `List[str]`
            A list containing all stations for which the positional data should be returned
        
        Returns
        -------
        `application/JSON`
            The positional data for the given stations (latitude in [degrees], longitude in [degrees], elevation in [meters])
        """
        pass