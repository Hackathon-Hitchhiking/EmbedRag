from abc import ABC, abstractmethod

from schemas.integrations import PageResponse


class BaseIntegrator(ABC):
    """
    A base class for integrating with different documentation platforms.
    """

    @abstractmethod
    def fetch_data(self, page_id: str) -> PageResponse:
        """
        Download a page given its ID.
        """
        pass

    @abstractmethod
    def close(self):
        pass
