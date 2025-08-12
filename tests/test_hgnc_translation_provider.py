from gene_thesaurus.hgnc_translation_provider import HgncException, HgncTranslationProvider
import pytest
import tempfile
from datetime import datetime
from freezegun import freeze_time


@freeze_time("2023-02-05 12:00:00")
def test_get_last_n_months():
    data_end_time = datetime.now()

    months = HgncTranslationProvider._get_last_n_months(data_end_time, 6)
    expected_months = ["2023-02", "2023-01", "2022-12",
                       "2022-11", "2022-10", "2022-09"]
    assert months == expected_months

    months = HgncTranslationProvider._get_last_n_months(data_end_time, 1)
    expected_months = ["2023-02"]
    assert months == expected_months


@freeze_time("2081-04-05 12:00:00")
def test_hgnc_exception():
    with pytest.raises(HgncException):
        data_dir = tempfile.TemporaryDirectory()
        data_dir_name = data_dir.name
        hgnc = HgncTranslationProvider(data_dir=data_dir_name,
                                       data_end_date = datetime.now(),
                                       n_attempted_months=2)

