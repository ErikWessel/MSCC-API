import datetime
from abc import ABC, abstractmethod

from fastapi.security import HTTPBasicCredentials

from aimlsse_api.data import QueryStates


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
    async def queryProductsMetadata(self, footprint:str, datetime_from:datetime, datetime_to:datetime,
        credentials:HTTPBasicCredentials):
        """
        Query products from the specified datetime-interval [datetime_from, datetime_to]
        
        Products contain metadata, allowing the user to filter before making a download request
        
        Parameters
        ----------
        footprint: `str`
            The point or polygon area of interest
        datetime_from: `datetime.datetime`
            The beginning of the interval to be queried
        datetime_to: `datetime.datetime`
            The end of the interval to be queried
        credentials: `HTTPBasicCredentials`
            A pydantic object with username and password strings
        
        Returns
        -------
        `application/JSON`
            The products that are queried from the data source for the given datetime-interval
        """
        pass

    @abstractmethod
    async def requestProduct(self, id:str, credentials:HTTPBasicCredentials):
        """
        Makes a request for the product with the specified id for the user with the given credentials.

        Returns the status of the request.
        
        Parameters
        ----------
        id: `str`
            The id of the product to be requested
        credentials: `HTTPBasicCredentials`
            A pydantic object with username and password strings
        
        Returns
        -------
        `application/JSON`
            The state of the request
        """
        pass
    
    @abstractmethod
    async def extractFeatures(self, id:str, radius:float, data:dict):
        """
        Requests the features to be extracted from the product with the specified id for the given:
        - frequency-bands of the measurement instruments
        - locations with an area of the given radius in the specified
        Coordinate Reference System (CRS)

        Returns a zip-file of the extracted features
        
        Parameters
        ----------
        id: `str`
            The id of the product to be requested
        radius: `float` [m]
            The radius around the locations for cropping
        data: `dict`
            - bands: `List[str]` The frequency-bands to extract the features for - e.g. ["B2", "B8A"]
            - locations: `application/JSON` The geo-spacial positions - each in the center of their own cropped data
            - crs: `str` The CRS for the given locations - e.g. "EPSG:4326" for latitude, longitude pairs
        
        Returns
        -------
        `application/zip`
            The zip-file of the extracted features
        """
        pass
    
    @abstractmethod
    async def getProduct(self, id:str):
        """
        Requests the full product with the specified id.

        Returns a zip-file of the product.
        
        Parameters
        ----------
        id: `str`
            The id of the product to be requested
        
        Returns
        -------
        `application/zip`
            The zip-file of the product
        """
        pass
