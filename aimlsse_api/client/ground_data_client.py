import logging
from datetime import date, datetime
from ipaddress import ip_address
from typing import List, Optional

import geopandas as gpd
import pandas as pd
import requests
from aimlsse_api.data.metar import (MetarPandas, MetarProperty,
                                    MetarPropertyType)
from dacite import from_dict
from shapely import Point, Polygon

from .web_client import WebClient


class GroundDataClient (WebClient):

    def __init__(self, ip_address: ip_address, port: int) -> None:
        super().__init__(ip_address, port)
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
    """
    Provides access to station based data of the ground-measurements data-source

    Hides communication with the service that implements `aimlsse_api.interface.GroundDataAccess` from the user
    """

    def queryMetar(self, datetime_from:datetime, datetime_to:datetime, properties:List[MetarProperty],
        stations:Optional[List[str]] = None, polygons:Optional[List[Polygon]] = None) -> pd.DataFrame:
        """
        Query data for the specified stations in the interval [datetime_from, datetime_to],
        where the properties are extracted from the METARs.

        Specify a list of stations, polygons or both for the query.
        
        Parameters
        ----------
        datetime_from: `datetime.datetime`
            The beginning of the interval to be queried
        datetime_to: `datetime.datetime`
            The end of the interval to be queried
        properties: `List[MetarProperty]`
            The properties to extract from the METARs
        stations: `Optional[List[str]]`
            A list containing all stations that the data should be queried for
        polygons: `Optional[List[Polygon]]`
            A list of polygons that specify the area to search for stations
        
        Returns
        -------
        `pandas.DataFrame`
            The METAR data that is queried from the data source for the given datetime-interval
            (station, datetime, ..requested properties..)
        """
        if stations is None and polygons is None:
            raise ValueError('No stations or polygons were given. Specify at least one of them.')
        data_json_out = {
            'properties': [str(prop) for prop in properties]
        }
        if stations:
            data_json_out['stations'] = stations
        if polygons:
            data_json_out['polygons'] = [str(x) for x in polygons]
        self.logger.debug(data_json_out)
        query_response = requests.post(f'{self.base_url}/queryMetar',
            params={'datetime_from': datetime_from, 'datetime_to': datetime_to}, json=data_json_out, stream=True)
        query_response.raise_for_status()
        data = pd.read_json(query_response.text, orient='table')
        data['datetime'] = pd.to_datetime(data['datetime'])
        data = MetarPandas.format_dataframe(data, properties)
        return data
    
    def queryMetadata(self, stations:Optional[List[str]] = None, polygons:Optional[List[Polygon]] = None):
        """
        Query metadata for the specified stations in the interval [date_from, date_to]

        Specify a list of stations, polygons or both for the query.
        
        Parameters
        ----------
        stations: `Optional[List[str]]`
            A list containing all stations for which the metadata should be returned
        polygons: `Optional[List[Polygon]]`
            A list of polygons that specify the area to search for stations
        
        Returns
        -------
        `geopandas.GeoDataFrame`
            The metadata for the given stations (latitude in [degrees], longitude in [degrees], elevation in [meters], ..)
        """
        if stations is None and polygons is None:
            raise ValueError('No stations or polygons were given. Specify at least one of them.')
        data_json_out = {}
        if stations:
            data_json_out['stations'] = stations
        if polygons:
            data_json_out['polygons'] = [str(x) for x in polygons]
        self.logger.debug(data_json_out)
        query_response = requests.post(f'{self.base_url}/queryMetadata', json=data_json_out)
        query_response.raise_for_status()
        data_json = query_response.json()
        geo_data = gpd.GeoDataFrame.from_features(data_json)
        return geo_data
