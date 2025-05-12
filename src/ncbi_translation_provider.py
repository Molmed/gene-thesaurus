import requests
import os
import pandas as pd
from typing import Literal
import logging
from src.translation_provider import TranslationProvider


class NcbiTranslationProvider(TranslationProvider):
    """
    NCBI Translation Provider for translating entrez ids to Ensembl ids or
    gene symbols.
    """
    _NCBI_BASE_URL = 'https://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/'  # noqa: E501
    _NCBI_FILENAME = 'Homo_sapiens.gene_info.gz'

    def __init__(self,
                 data_dir='/tmp'):
        self.__data_dir = data_dir
        self.__ncbi_gz_path = None
        self.__ncbi_data = None

        super().__init__(self.__data_dir)
        self.logger = logging.getLogger(__class__.__name__)
        self._get_ncbi_data()

    def _get_ncbi_data(self):
        self.__ncbi_gz_path = self.__data_dir + "/" + self._NCBI_FILENAME

        if not os.path.isfile(self.__ncbi_gz_path):
            url = self._NCBI_BASE_URL + self._NCBI_FILENAME
            self.logger.debug(f"Trying NCBI url: {url}")

            # 1 sec to connect, 10 sec to read
            r = requests.get(url, stream=True)
            with open(self.__ncbi_gz_path, 'wb') as f:
                f.write(r.content)

        # Load the data
        self.__ncbi_data = pd.read_csv(self.__ncbi_gz_path,
                                       sep='\t',
                                       compression='gzip')

    def translate_list(self,
                       gene_list: list,
                       source: TranslationProvider._IDENTIFIER_TYPES,
                       target: TranslationProvider._IDENTIFIER_TYPES) -> dict:
        valid = True
        if source == 'entrez_id':
            if target == 'symbol':
                return {}
            elif target == 'ensembl_id':
                return {}
            else:
                valid = False
        else:
            valid = False

        if not valid:
            err_msg = """Error: valid values for source and target are
            'symbol' and 'ensembl_id'."""
            raise ValueError(err_msg)
