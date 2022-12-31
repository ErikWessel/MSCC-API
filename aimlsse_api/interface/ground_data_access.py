import datetime
from abc import ABC, abstractmethod


class GroundDataAccess (ABC):
    """Provides access to geographical data of the ground-measurements data-source"""

    @abstractmethod
    async def queryMeasurements(self, datetime_from:datetime.datetime, datetime_to:datetime.datetime):
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
        `application/JSON`
            The data that is queried from the data source for the given datetime-interval
        """
        pass