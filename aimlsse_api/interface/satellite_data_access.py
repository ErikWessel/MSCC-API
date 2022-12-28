import datetime
from abc import ABC, abstractmethod


class SatelliteDataAccess (ABC):
    """Provides access to geographical data of the satellite's data-source"""

    @abstractmethod
    async def queryContainingGeometry(self, locations):
        """
        Query the geometry that together contain the provided locations

        Parameters
        ----------
        locations: `application/JSON`
            The geo-spacial positions to find the geometry for, that they are contained in
        
        Returns
        -------
        `application/JSON`
            The geometry that together contain the provided locations
        """
        pass

    @abstractmethod
    async def queryMeasurements(self, datetime_from:datetime.datetime, datetime_to:datetime.datetime, locations):
        """
        Query data from the specified datetime-interval [datetime_from, datetime_to]
        
        Parameters
        ----------
        datetime_from: `datetime.datetime`
            The beginning of the interval to be queried
        datetime_to: `datetime.datetime`
            The end of the interval to be queried
        locations: `application/JSON`
            The geo-spacial positions for which the data is queried
        
        Returns
        -------
        `application/JSON`
            The data that is queried from the data source for the given datetime-interval
        """
        pass