import pytest
import requests
import pathlib
from urllib.error import HTTPError
import xml.etree.ElementTree as ET
import xmltodict

LSS_DIR = pathlib.Path(__file__).parent / "run_files"
# names come from livesplit-core/tests/run_files/mod.rs
CELESTE = "Celeste - Any% (1.2.1.5).lss"
LIVESPLIT_1_0 = "livesplit1.0.lss"
LIVESPLIT_1_4 = "livesplit1.4.lss"
LIVESPLIT_1_5 = "livesplit1.5.lss"
LIVESPLIT_1_6_GAMETIME = "livesplit1.6_gametime.lss"
LIVESPLIT_1_6 = "livesplit1.6.lss"
LIVESPLIT_ATTEMPT_ENDED_BUG = "livesplit_attempt_ended_bug.lss"
LIVESPLIT_FUZZ_CRASH_UTF8 = "livesplit_fuzz_crash_utf8.lss"
LIVESPLIT_FUZZ_CRASH = "livesplit_fuzz_crash.lss"

VALID_SPLITS = [
    CELESTE,
    LIVESPLIT_1_0,
    LIVESPLIT_1_4,
    LIVESPLIT_1_5,
    LIVESPLIT_1_6_GAMETIME,
    LIVESPLIT_1_6,
]
INVALID_SPLITS = [
    LIVESPLIT_ATTEMPT_ENDED_BUG,
    LIVESPLIT_FUZZ_CRASH_UTF8,
    LIVESPLIT_FUZZ_CRASH,
]


def get_run_files(lss_dir: pathlib.Path) -> None:
    api_url = (
        "https://api.github.com/repos/LiveSplit/livesplit-core/contents/tests/run_files"
    )
    response = requests.get(api_url)
    files = response.json()

    lss_files = [file for file in files if file["name"].endswith(".lss")]
    for lss_file in lss_files:
        lss_src = lss_file["download_url"]
        lss_dst = lss_dir / lss_file["name"]

        if lss_dst.exists() and lss_dst.stat().st_size == lss_file["size"]:
            continue

        with requests.get(lss_src, stream=True) as response:
            response.raise_for_status()

            with open(lss_dst, "w", encoding="utf-8") as file:
                file.write(response.text)


@pytest.fixture
def ensure_presence_splits() -> bool:
    lss_names = VALID_SPLITS + INVALID_SPLITS
    lss_files = [LSS_DIR / lss_name for lss_name in lss_names]
    lss_present = all([lss_file.exists() for lss_file in lss_files])

    if not lss_present:
        try:
            get_run_files(lss_dir=LSS_DIR)
        except HTTPError as e:
            raise e
    return all([lss_file.exists() for lss_file in lss_files])


@pytest.fixture
def valid_splits(ensure_presence_splits):
    assert ensure_presence_splits
    return [LSS_DIR / split for split in VALID_SPLITS]


@pytest.fixture
def invalid_splits(ensure_presence_splits):
    assert ensure_presence_splits
    return [LSS_DIR / split for split in INVALID_SPLITS]


# not really possible to generate fixtures dynamically, just hardcode them here:
@pytest.fixture
def celeste_lsspath(ensure_presence_splits):
    assert ensure_presence_splits
    return LSS_DIR / CELESTE


@pytest.fixture
def livesplit_1_0_lsspath(ensure_presence_splits):
    assert ensure_presence_splits
    return LSS_DIR / LIVESPLIT_1_0


@pytest.fixture
def livesplit_1_4_lsspath(ensure_presence_splits):
    assert ensure_presence_splits
    return LSS_DIR / LIVESPLIT_1_4


@pytest.fixture
def livesplit_1_5_lsspath(ensure_presence_splits):
    assert ensure_presence_splits
    return LSS_DIR / LIVESPLIT_1_5


@pytest.fixture
def livesplit_1_6_gametime_lsspath(ensure_presence_splits):
    assert ensure_presence_splits
    return LSS_DIR / LIVESPLIT_1_6_GAMETIME


@pytest.fixture
def livesplit_1_6_lsspath(ensure_presence_splits):
    assert ensure_presence_splits
    return LSS_DIR / LIVESPLIT_1_6


@pytest.fixture
def livesplit_attempt_ended_bug_lsspath(ensure_presence_splits):
    assert ensure_presence_splits
    return LSS_DIR / LIVESPLIT_ATTEMPT_ENDED_BUG


@pytest.fixture
def livesplit_fuzz_crash_utf8_lsspath(ensure_presence_splits):
    assert ensure_presence_splits
    return LSS_DIR / LIVESPLIT_FUZZ_CRASH_UTF8


@pytest.fixture
def livesplit_fuzz_crash_lsspath(ensure_presence_splits):
    assert ensure_presence_splits
    return LSS_DIR / LIVESPLIT_FUZZ_CRASH
