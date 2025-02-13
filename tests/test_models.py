import pytest 
import lxml.etree as ET
from saltysplits.models import Splits, Metadata, Run, Platform, Variable, Attempt, Segment, SplitTime, BestSegmentTime, Time, AutoSplitterSettings, Split


class TestSplits:    
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        element = tree.getroot()
        element_string = ET.tostring(element, method='c14n2', strip_text=True) 
        # validating if we can instance from known valid XML element
        model = Splits.from_xml_tree(element)
        assert model == Splits.from_lss_file(livesplit_1_6_gametime_lsspath)
        recreated_element = model.to_xml_tree()
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string


class TestMetadata:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = root.find("Metadata")
        element_string = ET.tostring(element, method='c14n2', strip_text=True) 
        # validating if we can instance from known valid XML element
        model = Metadata.from_xml_tree(element)
        # we probably only want to set what's actually included in the given LSS, skip the rest?
        recreated_element = model.to_xml_tree() # This will drop elements like Region (which are expected)
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string

class TestRun:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = root.find("Metadata").find("Run")
        element_string = ET.tostring(element, method='c14n2', strip_text=True)
        # validating if we can instance from known valid XML element
        model = Run.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string


class TestPlatform:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = root.find("Metadata").find("Platform")
        element_string = ET.tostring(element, method='c14n2', strip_text=True)
        # validating if we can instance from known valid XML element
        model = Platform.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string
            
class TestVariable:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = next(root.iter("Variable"))
        element_string = ET.tostring(element, method='c14n2', strip_text=True)
        # validating if we can instance from known valid XML element
        model = Variable.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string


class TestAttempt:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = next(root.iter("Attempt"))
        element_string = ET.tostring(element, method='c14n2', strip_text=True)
        # maybe have a --verbose option that instantiates every possible Attempt model
        # validating if we can instance from known valid XML element
        model = Attempt.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string

class TestSegment:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = next(root.iter("Segment"))
        element_string = ET.tostring(element, method='c14n2', strip_text=True)
        # validating if we can instance from known valid XML element
        model = Segment.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element 
        assert element_string == recreated_element_string

class TestSplitTime:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = next(root.iter("SplitTime"))
        element_string = ET.tostring(element, method='c14n2', strip_text=True)
        # validating if we can instance from known valid XML element
        model = SplitTime.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element 
        assert element_string == recreated_element_string


class TestBestSegmentTime:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = next(root.iter("BestSegmentTime"))
        element_string = ET.tostring(element, method='c14n2', strip_text=True)
        # validating if we can instance from known valid XML element
        model = BestSegmentTime.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element 
        assert element_string == recreated_element_string


class TestTime:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = next(root.iter("Time"))
        element_string = ET.tostring(element, method='c14n2', strip_text=True)
        # validating if we can instance from known valid XML element
        model = Time.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element 
        assert element_string == recreated_element_string

class TestAutoSplitterSettings:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = next(root.iter("AutoSplitterSettings"))
        element_string = ET.tostring(element, method='c14n2', strip_text=True, with_comments=True)
        # validating if we can instance from known valid XML element
        model = AutoSplitterSettings.from_xml_tree(element)
        recreated_element = model.to_xml_tree()
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element 
        assert element_string == recreated_element_string
        #search_mode='ordered',
        # called get_unbound?


class TestSplit:
    def test_instancing(self, livesplit_1_6_gametime_lsspath):
        tree = ET.parse(livesplit_1_6_gametime_lsspath)
        root = tree.getroot()
        element = next(root.iter("Split"))
        element_string = ET.tostring(element, method='c14n2', strip_text=True)
        # validating if we can instance from known valid XML element
        model = Split.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, method='c14n2')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string
