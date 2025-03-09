from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path
from typing import List, Optional
from saltysplits.enums import TimeType
from saltysplits.annotations import encode_time
from saltysplits.models import Splits


class SaltySplits(Splits):
    @classmethod
    def read_lss(cls, lss_path: Path) -> SaltySplits:
        with open(lss_path, "rb") as file:
            xml_bytes = file.read()
        return cls.from_xml(xml_bytes)

    def _collect_ids(self) -> List[Optional[str]]:
        # run_ids can be found in attempt_history and/or each segment's segment_history (mainly due to deleted or otherwise partial attempts)
        run_ids = set()
        run_ids.update([attempt.id for attempt in self.attempt_history])
        run_ids.update([split.id for segment in self.segments for split in segment.segment_history])
        run_ids = list(run_ids)

        # sort them as int if possible
        if all(map(lambda x: str(int(x)) == x, run_ids)):
            run_ids = sorted(run_ids, key=lambda x: int(x))
        return run_ids
    
    def is_comparable(self, other: SaltySplits, strict: bool = True) -> bool:
        # checks if two SS instances shares the same game / category / segment names
        # strict also requires identical segment names (not just segment counts)
        same_game = self.game_name == other.game_name
        same_category = self.category_name == other.category_name
        same_count = len(self.segments) == len(other.segments)
        same_segments = all([self.segments[i].name == other.segments[i].name for i in range(len(self.segments))]) if same_count and strict else not strict
        return all([same_game, same_category, same_count, same_segments])
            
    def to_df(self, time_type: TimeType = TimeType.REAL_TIME, allow_partial: bool = False, allow_empty: bool = False, cumulative: bool = False, lss_repr: bool = False, lss_ns: bool = True) -> pd.DataFrame:
        run_ids = self._collect_ids() 
        segment_names = [segment.name for segment in self.segments]
        placeholder_data = np.full((len(segment_names), len(run_ids)), np.timedelta64('NaT', 'ns'))
        placeholder_df = pd.DataFrame(placeholder_data, columns=run_ids, index=segment_names)
        
        for segment in self.segments:
            for split in segment.segment_history:
                if time_type == time_type.GAME_TIME:
                    time = split.game_time
                elif time_type == time_type.REAL_TIME:
                    time = split.real_time
                placeholder_df.loc[segment.name, split.id] = time
        
        if not allow_partial:
            # drops runs that have one or more NaT values (i.e. incomplete runs)
            placeholder_df = placeholder_df.loc[:, ~placeholder_df.isna().any()]
            
        if not allow_empty:
            # drops runs that only have NaT values (i.e. empty runs)
            placeholder_df = placeholder_df.loc[:, ~placeholder_df.isna().all()]

        if cumulative:
            # skipna ensures that we stop accumulating if we miss a split in beween
            placeholder_df = placeholder_df.apply(lambda column: column.cumsum(skipna=False))
        
        if lss_repr:
            # formats timedelta values to same string representation as used in LSS files
            placeholder_df = placeholder_df.map(lambda x: encode_time(x, include_ns=lss_ns) if pd.notna(x) else None) 

        return placeholder_df
