import pytest 
import xmltodict
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from saltysplits.models import Splits, Metadata, Run, Platform, Variable, Attempt, Segment, SplitTime, BestSegmentTime, Time, AutoSplitterSettings, Split


class TestSplits:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        element = tree.getroot()
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # validating if we can instance from known valid XML element
        model = Splits.from_xml_tree(element)
        assert model == Splits.from_lss_file(celeste_lsspath)
        recreated_element = model.to_xml_tree()
        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string

class TestMetadata:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = root.find("Metadata")
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # validating if we can instance from known valid XML element
        model = Metadata.from_xml_tree(element)
        # we probably only want to set what's actually included in the given LSS, skip the rest?
        recreated_element = model.to_xml_tree(skip_empty=True) # This will drop elements like Region (which are expected)
        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string

class TestRun:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = root.find("Metadata").find("Run")
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # validating if we can instance from known valid XML element
        model = Run.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string


class TestPlatform:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = root.find("Metadata").find("Platform")
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # validating if we can instance from known valid XML element
        model = Platform.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)

        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string
            
class TestVariable:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = next(root.iter("Variable"))
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # validating if we can instance from known valid XML element
        model = Variable.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)

        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string


class TestAttempt:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = next(root.iter("Attempt"))
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # maybe have a --verbose option that instantiates every possible Attempt model
        #element = next(root.iter("Attempt"))
        # validating if we can instance from known valid XML element
        model = Attempt.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)

        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string

class TestSegment:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = next(root.iter("Segment"))
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # validating if we can instance from known valid XML element
        model = Segment.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)

        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element 
        assert element_string == recreated_element_string

class TestSplitTime:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = next(root.iter("SplitTime"))
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        
        # validating if we can instance from known valid XML element
        model = SplitTime.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)

        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element 
        assert element_string == recreated_element_string


class TestBestSegmentTime:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = next(root.iter("BestSegmentTime"))
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # validating if we can instance from known valid XML element
        model = BestSegmentTime.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)

        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element 
        assert element_string == recreated_element_string


class TestTime:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = next(root.iter("Time"))
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # validating if we can instance from known valid XML element
        model = Time.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)

        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element 
        assert element_string == recreated_element_string

class TestAutoSplitterSettings:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = next(root.iter("AutoSplitterSettings"))
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # validating if we can instance from known valid XML element
        model = AutoSplitterSettings.from_xml_tree(element)
        # TODO check if we also need to set exclude_unset=True (or use skip_empty)
        recreated_element = model.to_xml_tree(exclude_none=True)
        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element 
        assert element_string == recreated_element_string


class TestSplit:
    def test_celeste(self, celeste_lsspath):
        tree = ET.parse(celeste_lsspath)
        root = tree.getroot()
        element = next(root.iter("Split"))
        element_string = ET.tostring(element, encoding='utf-8', method='xml')
        # validating if we can instance from known valid XML element
        model = Split.from_xml_tree(element)
        recreated_element = model.to_xml_tree(exclude_none=True)

        recreated_element_string = ET.tostring(recreated_element, encoding='utf-8', method='xml')
        # validating that encoded model is identical to original XML element
        assert element_string == recreated_element_string
