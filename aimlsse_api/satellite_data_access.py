import abc
import datetime
from fastapi import Request
from fastapi.responses import JSONResponse

class SatelliteDataAccess (abc.ABC):
    """Provides access to geographical data of the satellite's data-source"""

    @abc.abstractmethod
    async def queryContainingGeometry(self, locations:Request) -> JSONResponse:
        """
        Query the geometry that together contain the provided locations

        Parameters
        ----------
        locations: fastapi.Request <-- application/JSON <-- geopandas.GeoDataFrame
            The geo-spacial positions to find the geometry for, that they are contained in
        
        Returns
        -------
        fastapi.responses.JSONResponse
            The geometry that together contain the provided locations
        """
        pass

    @abc.abstractmethod
    async def queryMeasurements(self, datetime_from:datetime.datetime, datetime_to:datetime.datetime, locations:Request) -> JSONResponse:
        """
        Query data from the specified datetime-interval [datetime_from, datetime_to]
        
        Parameters
        ----------
        datetime_from: datetime.datetime
            The beginning of the interval to be queried
        datetime_to: datetime.datetime
            The end of the interval to be queried
        locations: fastapi.Request
            The geo-spacial positions for which the data is queried
        
        Returns
        -------
        fastapi.responses.JSONResponse <-- geopandas.GeoDataFrame
            The data that is queried from the data source for the given datetime-interval
        """
        pass