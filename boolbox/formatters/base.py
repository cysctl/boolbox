from abc import ABC, abstractmethod
from typing import Any


class Formatter(ABC):
    """
    Interface for all ANF polynomial formatters
    Every new formatter must inherit from this class and implement the 'format' method
    """

    @abstractmethod
    def format(self, polys: dict[int, str]) -> Any:
        """
        Formats the generated ANF polynomials into a specific output structure

        Args:
            polys: A dictionary where values are the generated ANF polynomial strings

        Returns:
            The formatted output
            The return type is 'Any' because different formatters might return different types
        """
        pass
