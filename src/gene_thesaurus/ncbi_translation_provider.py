import requests
import os
import pandas as pd
import logging
from gene_thesaurus.translation_provider import TranslationProvider


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

    def _subset_ncbi_data(self, gene_list: list) -> list:
        # Get all rows where GeneId is in the gene_list
        entrez_df = self.__ncbi_data[self.__ncbi_data['GeneID'].isin(gene_list)]

        # Sort entrez_df so that the GeneIds are in the same order as gene_list
        entrez_df = entrez_df.set_index('GeneID')
        entrez_df = entrez_df.reindex(gene_list)

        return entrez_df

    def _translate_list_to_symbol(self, gene_list: list) -> dict:
        entrez_df = self._subset_ncbi_data(gene_list)
        entrez_dict = entrez_df['Symbol'].fillna('').to_dict()
        return entrez_dict

    def _translate_list_to_ensembl_id(self, gene_list: list) -> dict:
        entrez_df = self._subset_ncbi_data(gene_list)
        entrez_df['ensembl_id'] = entrez_df['dbXrefs'].str.extract(
            r'Ensembl:(ENSG\d{11})')
        entrez_dict = entrez_df['ensembl_id'].fillna('').to_dict()
        # Sort the dictionary so that the keys are in the same order as gene_list
        return entrez_dict

    def translate_list(self,
                       gene_list: list,
                       source: TranslationProvider._IDENTIFIER_TYPES,
                       target: TranslationProvider._IDENTIFIER_TYPES) -> dict:
        # Cast list of ids to list of ints
        gene_list = [int(gene) for gene in gene_list]

        valid = True
        if source == 'entrez_id':
            if target == 'symbol':
                return self._translate_list_to_symbol(gene_list)
            elif target == 'ensembl_id':
                return self._translate_list_to_ensembl_id(gene_list)
            else:
                valid = False
        else:
            valid = False

        if not valid:
            err_msg = """Error: valid values for source and target are
            'symbol' and 'ensembl_id'."""
            raise ValueError(err_msg)

