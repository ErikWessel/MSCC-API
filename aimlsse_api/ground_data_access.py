import abc
import datetime
from fastapi.responses import JSONResponse

class GroundDataAccess (abc.ABC):
    """Provides access to geographical data of the ground-measurements data-source"""

    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    async def queryMeasurements(self, datetime_from:datetime.datetime, datetime_to:datetime.datetime) -> JSONResponse:
        """
        Query data from the specified datetime-interval [datetime_from, datetime_to]
        
        Parameters
        ----------
        datetime_from: datetime.datetime
            The beginning of the interval to be queried
        datetime_to: datetime.datetime
            The end of the interval to be queried
        
        Returns
        -------
        fastapi.responses.JSONResponse <-- GeoDataFrame
            The data that is queried from the data source for the given datetime-interval
        """
        pass