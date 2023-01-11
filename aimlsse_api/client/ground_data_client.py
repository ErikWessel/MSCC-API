from datetime import date
from typing import List

import pandas as pd
import requests

from .web_client import WebClient


class GroundDataClient (WebClient):
    """
    Provides access to station based data of the ground-measurements data-source

    Hides communication with the service that implements `aimlsse_api.interface.GroundDataAccess` from the user
    """

    def queryMetar(self, stations:List[str], date_from:date, date_to:date) -> pd.DataFrame:
        """
        Query data for the specified stations in the interval [date_from, date_to]
        
        Parameters
        ----------
        stations: `List[str]`
            A list containing all stations that the data should be queried for
        date_from: `datetime.date`
            The beginning of the interval to be queried
        date_to: `datetime.date`
            The end of the interval to be queried
        
        Returns
        -------
        `pandas.DataFrame`
            The data that is queried from the data source for the given date-interval
        """
        query_response = requests.post(f'{self.base_url}/queryMetar',
            params={'date_from': date_from, 'date_to': date_to}, json=stations)
        query_response.raise_for_status()
        data_json = query_response.json()
        data = pd.DataFrame(data_json)
        data['datetime'] = pd.to_datetime(data['datetime'])
        return data
