import datetime
import json
import os
from typing import List, Optional, Union

import geopandas as gpd
import pandas as pd
import requests
from aimlsse_api.data import Credentials
from aimlsse_api.data.status import QueryStates
from requests.auth import HTTPBasicAuth
from shapely import Geometry, Point, Polygon

from . import WebClient


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

    def queryProductsMetadata(self, footprint:Union[Point, Polygon], datetime_from:datetime, datetime_to:datetime,
        copernicus_login:Credentials) -> pd.DataFrame:
        """
        Query products from the specified datetime-interval [datetime_from, datetime_to]
        
        Products contain metadata, allowing the user to filter before making a download request
        
        Parameters
        ----------
        footprint: `Union[Point, Polygon]`
            The point or polygon area of interest
        datetime_from: `datetime.datetime`
            The beginning of the interval to be queried
        datetime_to: `datetime.datetime`
            The end of the interval to be queried
        copernicus_login: `Credentials`
            The login information for the copernicus hub
        
        Returns
        -------
        `pandas.DataFrame`
            The products that are queried from the data source for the given datetime-interval
        """
        query_response = requests.post(f'{self.base_url}/queryProductsMetadata',
            params={
                'footprint': footprint.wkt,
                'datetime_from': datetime_from,
                'datetime_to': datetime_to
            },
            auth=HTTPBasicAuth(copernicus_login.username, copernicus_login.password),
            stream=True
        )
        query_response.raise_for_status()
        return pd.DataFrame(query_response.json())
    
    def requestProduct(self, id:str, copernicus_login:Credentials) -> QueryStates:
        """
        Makes a request for the product with the specified id for the user with the given credentials.

        Returns the status of the request.
        
        Parameters
        ----------
        id: `str`
            The id of the product to be requested
        copernicus_login: `Credentials`
            The login information for the copernicus hub
        
        Returns
        -------
        `QueryStates`
            The state of the request
        """
        query_response = requests.get(f'{self.base_url}/requestProduct',
            params={
                'id': id
            },
            auth=HTTPBasicAuth(copernicus_login.username, copernicus_login.password)
        )
        query_response.raise_for_status()
        data_json = query_response.json()
        return QueryStates(data_json['state'])

    def extractFeatures(self, id:str, radius:float, bands:List[str], locations:gpd.GeoDataFrame,
        out_dir:str) -> str:
        """
        Requests the features to be extracted from the product with the specified id for the given:
        - frequency-bands of the measurement instruments
        - locations with an area of the given radius in the specified
        Coordinate Reference System (CRS)

        Returns the path to the downloaded zip-file of the extracted features
        
        Parameters
        ----------
        id: `str`
            The id of the product to be requested
        radius: `float` [m]
            The radius around the locations for cropping
        bands: `List[str]`
            The frequency-bands to extract the features for - e.g. ["B2", "B8A"]
        locations: `geopandas.GeoDataFrame`
            The geo-spacial positions - each in the center of their own cropped data
        
        Returns
        -------
        `str`
            The path to the downloaded zip-file of the extracted features
        """
        os.makedirs(out_dir, exist_ok=True)
        filepath = os.path.join(out_dir, f'{id}.zip')
        with requests.post(f'{self.base_url}/extractFeatures',
            params={
                'id': id,
                'radius': radius
            },
            json={
                'bands': bands,
                'locations': json.loads(locations.to_json()),
                'crs': str(locations.crs)
            },
            stream=True
        ) as response:
            response.raise_for_status()
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content():
                    file.write(chunk)
        return filepath
