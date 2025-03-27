import pathlib 
from .main import SaltySplits
from .enums import TimeType
from functools import partial as _partial

#DEMO_SPLITS = pathlib.Path( __file__).parents[1] / "tests/run_files/Grand Theft Auto Vice City - Any% (No SSU).lss"
DEMO_SPLITS = pathlib.Path( __file__).parents[1] / "tests/run_files/gcb.lss"

# forwarding read_lss to main module (+ docs)
read_lss = _partial(SaltySplits.read_lss)
read_lss.__doc__ = SaltySplits.read_lss.__doc__