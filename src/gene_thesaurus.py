from datetime import datetime, timedelta
import os.path
import requests
import json
import logging


class HgncException(Exception):
    def __init__(self, message="Could not obtain HGNC data."):
        self.message = message
        super().__init__(self.message)


class GeneThesaurus:
    _HGNC_BASE_URL = 'https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/monthly/json/'  # noqa: E501
    _HGNC_BASE_FILENAME = 'hgnc_complete_set_{month}-01.json'
    _SYMBOL_THESAURUS_BASE_FILENAME = 'symbol_thesaurus_{month}-01.json'
    _SYMBOL_TO_ENSEMBL_DICT_BASE_FILENAME = 'symbol_to_ensembl_{month}-01.json'
    _ENSEMBL_TO_SYMBOL_DICT_BASE_FILENAME = 'ensembl_to_symbol_{month}-01.json'

    def __init__(self,
                 data_dir='/tmp',
                 data_end_date=datetime.now(),
                 n_attempted_months=6):

        # Logging
        self.logger = logging.getLogger(__class__.__name__)

        # Data
        self.__data_dir = data_dir
        self.__data_end_date = data_end_date
        self.__n_attempted_months = n_attempted_months
        self.__hgnc_data_month = None
        self.__hgnc_json_path = None
        self.__hgnc_data = None

        # Try getting HGNC data for the past n months
        months = self._get_last_n_months(self.__data_end_date,
                                         self.__n_attempted_months)

        for month in months:
            filename = self._HGNC_BASE_FILENAME.format(month=month)
            path = self.__data_dir + "/" + filename
            found = False

            if os.path.isfile(path):
                found = True
            else:
                url = self._HGNC_BASE_URL + filename
                r = requests.get(url)
                if r.status_code == 200:
                    found = True
                    with open(path, 'wb') as f:
                        f.write(r.content)

            if found:
                self.__hgnc_data_month = month
                self.__hgnc_json_path = path
                break

        # If we have maxed out number of attempts, throw exception
        if not self.__hgnc_data_month or not self.__hgnc_json_path:
            raise HgncException(
                f"Could not retrieve HGNC data from {self._HGNC_BASE_URL}")

        # Load the HGNC JSON data
        with open(self.__hgnc_json_path, 'r', encoding='utf8') as f:
            data = json.loads(f.read())
            self.__hgnc_data = data['response']['docs']

    @staticmethod
    def _get_last_n_months(data_end_date, n_months):
        return [(data_end_date - timedelta(days=30 * i)).
                strftime('%Y-%m') for i in range(n_months)]

    def update_gene_symbols(self, gene_list):
        """
        Returns the latest gene symbols for the given list of gene names.

        Args:
            gene_list (list): A list of gene symbols to update.

        Returns:
            dict: A dictionary mapping each gene to its update gene symbol.
        """
        self.__symbol_thesaurus = None

        # Prepare the thesaurus, where each 'symbol', 'prev_symbol'
        # and 'alias_symbol' all map to 'symbol'
        dict_filename = self._SYMBOL_THESAURUS_BASE_FILENAME.format(
            month=self.__hgnc_data_month)
        dict_json_path = self.__data_dir + "/" + dict_filename

        # Does it already exist?
        if os.path.isfile(dict_json_path):
            with open(dict_json_path, 'r', encoding='utf8') as f:
                self.__symbol_thesaurus = json.loads(f.read())
        else:
            self.__symbol_thesaurus = {}
            for item in self.__hgnc_data:
                # The current gene name
                symbol = item.get("symbol")
                self.__symbol_thesaurus[symbol] = symbol

                # Optionally available older synonyms
                prev_symbols = item.get("prev_symbol", [])
                for sym in prev_symbols:
                    self.__symbol_thesaurus[sym] = symbol
                alias_symbols = item.get("alias_symbol", [])
                for sym in alias_symbols:
                    self.__symbol_thesaurus[sym] = symbol

            # Save the thesaurus
            with open(dict_json_path, 'w') as file:
                json.dump(self.__symbol_thesaurus, file)

        return {key: self.__symbol_thesaurus[key] for key in gene_list
                if key in self.__symbol_thesaurus and
                key != self.__symbol_thesaurus[key]}

    def _translate_ensembl_ids_to_symbols(self, gene_list):
        """
        Translates a list of Ensembl IDs to gene symbols.

        Args:
            gene_list (list): A list of Ensembl IDs to be translated.

        Returns:
            dict: A dictionary mapping each Ensembl ID to its gene symbol.
        """
        self.__ensembl_to_symbol_dict = None

        # Prepare the dinctionary, where each 'ensembl_id' maps to 'symbol'
        dict_filename = self._ENSEMBL_TO_SYMBOL_DICT_BASE_FILENAME.format(
            month=self.__hgnc_data_month)
        dict_json_path = self.__data_dir + "/" + dict_filename

        # Does it already exist?
        if os.path.isfile(dict_json_path):
            with open(dict_json_path, 'r', encoding='utf8') as f:
                self.__ensembl_to_symbol_dict = json.loads(f.read())
        else:
            self.__ensembl_to_symbol_dict = {}
            for item in self.__hgnc_data:
                # The ensembl id
                ensembl_id = item.get("ensembl_gene_id")

                # The current gene name
                symbol = item.get("symbol")
                self.__ensembl_to_symbol_dict[ensembl_id] = symbol

            # Save the dict
            with open(dict_json_path, 'w') as file:
                json.dump(self.__ensembl_to_symbol_dict, file)

        return {key: self.__ensembl_to_symbol_dict[key] for key in gene_list
                if key in self.__ensembl_to_symbol_dict and
                key != self.__ensembl_to_symbol_dict[key]}

    def _translate_symbols_to_ensembl_ids(self, gene_list):
        """
        Translates a list of gene symbols to Ensembl IDs.

        Args:
            gene_list (list): A list of gene symbols to be translated.

        Returns:
            dict: A dictionary mapping each gene symbol to its Ensembl ID.
        """
        self.__symbol_to_ensembl_dict = None

        # Prepare the dinctionary, where each 'symbol', 'prev_symbol'
        # and 'alias_symbol' all map to 'ensembl_id'
        dict_filename = self._SYMBOL_TO_ENSEMBL_DICT_BASE_FILENAME.format(
            month=self.__hgnc_data_month)
        dict_json_path = self.__data_dir + "/" + dict_filename

        # Does it already exist?
        if os.path.isfile(dict_json_path):
            with open(dict_json_path, 'r', encoding='utf8') as f:
                self.__symbol_to_ensembl_dict = json.loads(f.read())
        else:
            self.__symbol_to_ensembl_dict = {}
            for item in self.__hgnc_data:
                # The ensembl id
                ensembl_id = item.get("ensembl_gene_id")

                # The current gene name
                symbol = item.get("symbol")
                self.__symbol_to_ensembl_dict[symbol] = ensembl_id

                # Optionally available older synonyms
                prev_symbols = item.get("prev_symbol", [])
                for sym in prev_symbols:
                    self.__symbol_to_ensembl_dict[sym] = ensembl_id
                alias_symbols = item.get("alias_symbol", [])
                for sym in alias_symbols:
                    self.__symbol_to_ensembl_dict[sym] = ensembl_id

            # Save the dict
            with open(dict_json_path, 'w') as file:
                json.dump(self.__symbol_to_ensembl_dict, file)

        return {key: self.__symbol_to_ensembl_dict[key] for key in gene_list
                if key in self.__symbol_to_ensembl_dict and
                key != self.__symbol_to_ensembl_dict[key]}

    def translate_genes(self, gene_list, source='symbol', target='ensembl_id'):
        """
        Translates a list of genes from the source to the target format.
        Valid values for source and target are 'symbol' and 'ensembl_id'.

        Args:
            gene_list (list): A list of gene names to be translated.
            source (str): The format of the input genes. Defaults to 'symbol'.
            target (str): The format of the output genes.
            Defaults to 'ensembl_id'.

        Returns:
            dict: A dictionary mapping each source gene to its target format.
        """

        if source == 'symbol' and target == 'ensembl_id':
            return self._translate_symbols_to_ensembl_ids(gene_list)
        elif source == 'ensembl_id' and target == 'symbol':
            return self._translate_ensembl_ids_to_symbols(gene_list)
        else:
            err_msg = """Error: valid values for source and target are
            'symbol' and 'ensembl_id'."""
            raise ValueError(err_msg)
