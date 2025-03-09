import pathlib 
from .main import SaltySplits
from .enums import TimeType

#DEMO_SPLITS = pathlib.Path( __file__).parents[1] / "tests/run_files/Grand Theft Auto Vice City - Any% (No SSU).lss"
DEMO_SPLITS = pathlib.Path( __file__).parents[1] / "tests/run_files/gcb.lss"

# TODO docstrings are not passed through now (check update_wrapper)
read_lss = SaltySplits.read_lss
