import os
import pathlib

import pytest

match_dagid_filename_testfilesdir = os.path.join(pytest.helpers.file_abspath(__file__), "scripts")
match_dagid_filename_testfiles = list(pathlib.Path(match_dagid_filename_testfilesdir).glob("**/*.py"))


@pytest.mark.parametrize(
    "test_filepath",
    match_dagid_filename_testfiles,
    ids=[
        str(p.relative_to(match_dagid_filename_testfilesdir))
        for p in match_dagid_filename_testfiles
    ],
)
def test_match_dagid_filename(test_filepath):
    pytest.helpers.functional_test(test_filepath)
