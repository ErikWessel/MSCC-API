import datetime
from typing import Union

import geopandas as gpd
import requests

from .web_client import WebClient


class GroundDataClient (WebClient):
    """
    Provides access to geographical data of the ground-measurements data-source

    Hides communication with the service that implements `aimlsse_api.interface.GroundDataAccess` from the user
    """

    def queryMeasurements(self, datetime_from:datetime.datetime, datetime_to:datetime.datetime) -> gpd.GeoDataFrame:
        """
        Query data from the specified datetime-interval [datetime_from, datetime_to]
        
        Parameters
        ----------
        datetime_from: `datetime.datetime`
            The beginning of the interval to be queried
        datetime_to: `datetime.datetime`
            The end of the interval to be queried
        
        Returns
        -------
        `geopandas.GeoDataFrame`
            The data that is queried from the data source for the given datetime-interval
        """
        query_response = requests.get(f'{self.base_url}/queryMeasurements',
            params={'datetime_from': datetime_from, 'datetime_to': datetime_to})
        query_response.raise_for_status()
        data_json = query_response.json()
        return gpd.GeoDataFrame.from_features(data_json['features'])
