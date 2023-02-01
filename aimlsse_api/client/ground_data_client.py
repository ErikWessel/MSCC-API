import logging
from datetime import date
from ipaddress import ip_address
from typing import List

import geopandas as gpd
import pandas as pd
import requests
from aimlsse_api.data.metar import (MetarPandas, MetarProperty,
                                    MetarPropertyType)
from dacite import from_dict
from shapely import Point

from .web_client import WebClient


class GroundDataClient (WebClient):

    def __init__(self, ip_address: ip_address, port: int) -> None:
        super().__init__(ip_address, port)
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
    """
    Provides access to station based data of the ground-measurements data-source

    Hides communication with the service that implements `aimlsse_api.interface.GroundDataAccess` from the user
    """

    def queryMetar(self, stations:List[str], date_from:date, date_to:date, properties:List[MetarProperty]) -> pd.DataFrame:
        """
        Query data for the specified stations in the interval [date_from, date_to],
        where the properties are extracted from the METARs.
        
        Parameters
        ----------
        stations: `List[str]`
            A list containing all stations that the data should be queried for
        date_from: `datetime.date`
            The beginning of the interval to be queried
        date_to: `datetime.date`
            The end of the interval to be queried
        properties: `List[MetarProperty]`
            The properties to extract from the METARs
        
        Returns
        -------
        `pandas.DataFrame`
            The METAR data that is queried from the data source for the given date-interval
            (station, datetime, ..requested properties..)
        """
        data_json_out = {
            'stations': stations,
            'properties': [str(prop) for prop in properties]
        }
        print(data_json_out)
        query_response = requests.post(f'{self.base_url}/queryMetar',
            params={'date_from': date_from, 'date_to': date_to}, json=data_json_out, stream=True)
        query_response.raise_for_status()
        data_json_in = query_response.json()
        data = pd.DataFrame(data_json_in)
        data['datetime'] = pd.to_datetime(data['datetime'])
        data = MetarPandas.format_dataframe(data, properties)
        return data
    
    def queryPosition(self, stations:List[str]):
        """
        Query data for the specified stations in the interval [date_from, date_to]
        
        Parameters
        ----------
        stations: `List[str]`
            A list containing all stations for which the positional data should be returned
        
        Returns
        -------
        `geopandas.GeoDataFrame`
            The positional data for the given stations (latitude in [degrees], longitude in [degrees], elevation in [meters])
        """
        query_response = requests.post(f'{self.base_url}/queryPosition', json=stations)
        query_response.raise_for_status()
        data_json = query_response.json()
        data = pd.DataFrame(data_json)
        data['geometry'] = data.apply(lambda x: Point(x['longitude'], x['latitude']), axis=1)
        geo_data = gpd.GeoDataFrame(data, geometry='geometry', crs='epsg:4326')
        return geo_data
