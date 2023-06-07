from gene_thesaurus import gene_thesaurus

def test_lookup():
    test_genes = ['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP']
    symbols = gene_thesaurus.lookup(test_genes)
    assert symbols == ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C']
