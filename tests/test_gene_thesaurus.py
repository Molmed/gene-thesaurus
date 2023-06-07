from gene_thesaurus import gene_thesaurus
import tempfile

def test_lookup():
    test_genes = ['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP']
    data_dir = "/tmp" #tempfile.TemporaryDirectory().name
    symbols = gene_thesaurus.lookup(test_genes, data_dir=data_dir)
    assert symbols == ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C']
