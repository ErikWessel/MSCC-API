import datetime
import json

import geopandas as gpd
import requests

from .web_client import WebClient


class SatelliteDataClient (WebClient):
    """
    Provides access to geographical data of the ground-measurements data-source

    Hides communication with the service that implements `aimlsse_api.interface.SatelliteDataAccess` from the user
    """

    def queryContainingGeometry(self, locations:gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Query the geometry that together contain the provided locations

        Parameters
        ----------
        locations: `geopandas.GeoDataFrame`
            The geo-spacial positions to find the geometry for, that they are contained in
        
        Returns
        -------
        `geopandas.GeoDataFrame`
            The geometry that together contain the provided locations
        """
        locations_json = json.loads(locations.to_json())
        query_response = requests.post(f'{self.base_url}/queryContainingGeometry', json=locations_json)
        query_response.raise_for_status()
        geometry_json = query_response.json()
        return gpd.GeoDataFrame.from_features(geometry_json['features'])

    def queryMeasurements(self, datetime_from:datetime.datetime, datetime_to:datetime.datetime, locations:gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Query data from the specified datetime-interval [datetime_from, datetime_to]
        
        Parameters
        ----------
        datetime_from: `datetime.datetime`
            The beginning of the interval to be queried
        datetime_to: `datetime.datetime`
            The end of the interval to be queried
        locations: `geopandas.GeoDataFrame`
            The geo-spacial positions for which the data is queried
        
        Returns
        -------
        `geopandas.GeoDataFrame`
            The data that is queried from the data source for the given datetime-interval
        """
        raise NotImplementedError("Data access is not available yet!")