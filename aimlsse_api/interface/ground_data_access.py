import datetime
from abc import ABC, abstractmethod
from datetime import date
from typing import List


class GroundDataAccess (ABC):
    """Provides access to station data of the ground-measurements data-source"""

    @abstractmethod
    async def queryMetar(self, stations:List[str], date_from:date, date_to:date):
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
        `application/JSON`
            The data that is queried from the data source for the given date-interval
        """
        pass