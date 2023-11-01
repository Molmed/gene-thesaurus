import gene_thesaurus
import tempfile
from freezegun import freeze_time

data_dir = tempfile.TemporaryDirectory()
data_dir_name = data_dir.name


@freeze_time("2023-11-15 12:00:00")
def test_get_month_random_day():
    assert gene_thesaurus.get_month() == "2023-11"


@freeze_time("2023-11-01 12:00:00")
def test_get_month_first_day():
    assert gene_thesaurus.get_month() == "2023-10"


def test_translate_genes():
    test_genes = ['TNFSF2', 'ERBB1', 'VPF', 'ZSCAN5CP']
    symbols = gene_thesaurus.translate_genes(test_genes,
                                             data_dir=data_dir_name)
    assert symbols == ['TNF', 'EGFR', 'VEGFA', 'ZSCAN5C']


def test_translate_invalid_genes():
    test_genes = ['TNFSF2', 'ERBB1', 'NOTAREALGENE', 'ZSCAN5CP']
    symbols = gene_thesaurus.translate_genes(test_genes,
                                             data_dir=data_dir_name)
    assert symbols == ['TNF', 'EGFR', 'NOTAREALGENE', 'ZSCAN5C']


def test_translate_invalid_genes_nullify_missing():
    test_genes = ['TNFSF2', 'ERBB1', 'NOTAREALGENE', 'ZSCAN5CP']
    symbols = gene_thesaurus.translate_genes(test_genes,
                                             data_dir=data_dir_name,
                                             nullify_missing=True)
    assert symbols == ['TNF', 'EGFR', None, 'ZSCAN5C']
