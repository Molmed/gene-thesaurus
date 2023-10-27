from gene_thesaurus import gene_thesaurus
import tempfile
import os

data_dir = tempfile.TemporaryDirectory()
data_dir_name = data_dir.name

def test_lookup():
    test_genes = ['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP']
    symbols = gene_thesaurus.lookup(test_genes, data_dir=data_dir_name)
    assert symbols == ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C']

def test_invalid_lookup():
    test_genes = ['TNFSF2', 'ERBB1', 'NOTAREALGENE', 'ZSCAN5CP']
    symbols = gene_thesaurus.lookup(test_genes, data_dir=data_dir_name)
    assert symbols == ['TNF', 'EGFR', None, 'ZSCAN5C']
