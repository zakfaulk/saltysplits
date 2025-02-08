import pytest 
from saltysplits.models import Splits
from xml.etree.ElementTree import ParseError

class TestSplits:
    def test_all_valid(self, valid_splits):
        for valid_split in valid_splits:
            with open(valid_split, "r", encoding="utf-8") as file:
                xml_string = file.read()
            Splits.from_xml(xml_string)

    def test_all_invalid(self, invalid_splits):
        for invalid_split in invalid_splits:
            with open(invalid_split, "r", encoding="utf-8") as file:
                xml_string = file.read()
        
            with pytest.raises(ParseError):
                Splits.from_xml(xml_string)
