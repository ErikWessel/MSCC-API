import ipaddress
from abc import ABC
from typing import Union


class WebClient(ABC):
    IPAddress = Union[ipaddress.IPv4Address, ipaddress.IPv6Address]

    def __init__(self, ip_address:IPAddress, port:int) -> None:
        """
        Uses the provided ip-address and port to access a service that implements the corresponding interface

        Parameters
        ----------
        ip_address: `AllowedIPAddress`
            The ip-address under which the service is available
        port: `int`
            The port under which the service is available
        """
        self.base_url = f"http://{ip_address}:{port}"