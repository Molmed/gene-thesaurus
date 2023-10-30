import gene_thesaurus
import tempfile
import os

data_dir = tempfile.TemporaryDirectory()
data_dir_name = data_dir.name

def test_translate_genes():
    test_genes = ['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP']
    symbols = gene_thesaurus.translate_genes(test_genes, data_dir=data_dir_name)
    assert symbols == ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C']

def test_translate_invalid_genes():
    test_genes = ['TNFSF2', 'ERBB1', 'NOTAREALGENE', 'ZSCAN5CP']
    symbols = gene_thesaurus.translate_genes(test_genes, data_dir=data_dir_name)
    assert symbols == ['TNF', 'EGFR', 'NOTAREALGENE', 'ZSCAN5C']

def test_translate_invalid_genes_nullify_missing():
    test_genes = ['TNFSF2', 'ERBB1', 'NOTAREALGENE', 'ZSCAN5CP']
    symbols = gene_thesaurus.translate_genes(test_genes, data_dir=data_dir_name, nullify_missing=True)
    assert symbols == ['TNF', 'EGFR', None, 'ZSCAN5C']
