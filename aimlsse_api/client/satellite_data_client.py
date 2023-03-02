import datetime
import json
import os
import re
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

    def queryProductsMetadata(self, datetime_from:datetime.datetime, datetime_to:datetime.datetime,
        copernicus_login:Credentials, footprint:Optional[Union[Point, Polygon]] = None,
        cell_name:Optional[str] = None) -> pd.DataFrame:
        """
        Query products from the specified datetime-interval [datetime_from, datetime_to]
        
        Products contain metadata, allowing the user to filter before making a download request

        It is required to specify either the footprint or the cell_name!
        
        Parameters
        ----------
        datetime_from: `datetime.datetime`
            The beginning of the interval to be queried
        datetime_to: `datetime.datetime`
            The end of the interval to be queried
        copernicus_login: `Credentials`
            The login information for the copernicus hub
        footprint: `Union[Point, Polygon]`
            The point or polygon area of interest
        cell_name: `str`
            The name of a L1C grid cell

        Returns
        -------
        `pandas.DataFrame`
            The products that are queried from the data source for the given datetime-interval
        """
        json_out = {}
        if footprint is not None:
            json_out['footprint'] = footprint.wkt
        elif cell_name is not None:
            json_out['cell_name'] = cell_name
        else:
            raise ValueError('It is required to specify either the footprint or the cell_name!')
        query_response = requests.post(f'{self.base_url}/queryProductsMetadata',
            params={
                'datetime_from': datetime_from,
                'datetime_to': datetime_to
            },
            json=json_out,
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
        out_dir: `str`
            The directory in which to store the incoming data
        
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
                for chunk in response.iter_content(512 * 1024):
                    file.write(chunk)
        return filepath

    def getProduct(self, id:str, out_dir:str):
        """
        Requests the full product with the specified id.

        Returns a zip-file of the product.
        
        Parameters
        ----------
        id: `str`
            The id of the product to be requested
        out_dir: `str`
            The directory in which to store the incoming data
        
        Returns
        -------
        `str`
            The path to the downloaded zip-file of the extracted features
        """
        os.makedirs(out_dir, exist_ok=True)
        with requests.get(f'{self.base_url}/getProduct',
            params={
                'id': id,
            }
        ) as response:
            response.raise_for_status()
            disposition_str = 'content-disposition'
            if disposition_str in response.headers:
                disposition = response.headers[disposition_str]
                filename = re.findall("filename=\"(.+)\"", disposition)[0]
            else:
                filename = f'{id}.zip'
            filepath = os.path.join(out_dir, filename)
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(512 * 1024):
                    file.write(chunk)
        return filepath