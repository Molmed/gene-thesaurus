import logging
from src.translation_provider import TranslationProvider
from src.hgnc_translation_provider import HgncTranslationProvider
from src.ncbi_translation_provider import NcbiTranslationProvider


class GeneThesaurus:
    def __init__(self,
                 data_dir='/tmp'):
        self.__data_dir = data_dir
        self.logger = logging.getLogger(__class__.__name__)

    def update_gene_symbols(self, gene_list):
        hgnc = HgncTranslationProvider(self.__data_dir)
        return hgnc.update_gene_symbols(gene_list)

    def translate_genes(self,
                        gene_list: list,
                        source: str = 'symbol',
                        target: str = 'ensembl_id'):
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

        # Extract valid values from the Literal type
        valid_identifier_types = TranslationProvider._IDENTIFIER_TYPES.__args__

        # Check the source and target
        if source not in valid_identifier_types:
            err_msg = f"""Error: source must be one of {
                valid_identifier_types}."""
            raise ValueError(err_msg)
        if target not in valid_identifier_types:
            err_msg = f"""Error: target must be one of {
                valid_identifier_types}."""
            raise ValueError(err_msg)
        if source == target:
            err_msg = "Error: source and target must be different."
            raise ValueError(err_msg)

        # Check the valid combinations
        valid_combination = False
        if source == 'symbol' and target == 'ensembl_id':
            valid_combination = True
        elif source == 'ensembl_id' and target == 'symbol':
            valid_combination = True
        elif source == 'entrez_id' and target == 'symbol':
            valid_combination = True
        elif source == 'entrez_id' and target == 'ensembl_id':
            valid_combination = True
        if not valid_combination:
            err_msg = """Error: valid combinations of source and target are
            'symbol' -> 'ensembl_id',
            'ensembl_id' -> 'symbol',
            'entrez_id' -> 'symbol',
            'entrez_id' -> 'ensembl_id'."""
            raise ValueError(err_msg)

        if source == 'symbol' or source == 'ensembl_id':
            hgnc = HgncTranslationProvider(self.__data_dir)
            return hgnc.translate_list(gene_list, source, target)

        elif source == 'entrez_id':
            ncbi = NcbiTranslationProvider(self.__data_dir)
            return ncbi.translate_list(gene_list, source, target)
