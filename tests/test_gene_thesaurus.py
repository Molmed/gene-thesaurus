from gene_thesaurus import gene_thesaurus
import tempfile
import os

def test_lookup():
    test_genes = ['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP']
    data_dir_name = os.getenv('RUNNER_TEMP', None)
    if not data_dir_name:
        data_dir = tempfile.TemporaryDirectory()
        data_dir_name = data_dir.name
    symbols = gene_thesaurus.lookup(test_genes, data_dir=data_dir_name)
    assert symbols == ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C']
