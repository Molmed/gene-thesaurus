from abc import ABC, abstractmethod
from typing import Literal
import logging


class TranslationProvider(ABC):
    """
    Abstract base class for translation providers.
    Subclasses must implement the translate_list method.
    """

    # Define accepted sources and targets
    _IDENTIFIER_TYPES = Literal[
        'symbol',
        'ensembl_id',
        'entrez_id',
    ]

    def __init__(self,
                 data_dir='/tmp'):

        # Logging
        self.logger = logging.getLogger(__class__.__name__)

        # Data
        self.__data_dir = data_dir

    @abstractmethod
    def translate_list(self,
                       gene_list: list,
                       source: _IDENTIFIER_TYPES,
                       target: _IDENTIFIER_TYPES) -> dict:
        pass
