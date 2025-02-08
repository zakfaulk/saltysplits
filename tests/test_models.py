import pytest 
import xmltodict
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError
from saltysplits.models import Splits, Metadata, Run, Platform, Variable, Attempt, Segment, SplitTime, BestSegmentTime, Time, AutoSplitterSettings


class TestSplits:
    def test_1_6(self, livesplit_1_6_lsspath):
        
        # from xml_file
        #Splits.from_lss_file(livesplit_1_6_lsspath)

        # from xml_tree
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        Splits.from_xml_tree(root)

class TestMetadata:
    def test_1_6(self, livesplit_1_6_lsspath):
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        element = root.find("Metadata")
        #metadata_string = ET.tostring(metadata_element, encoding='utf-8', method='xml') 
        Metadata.from_xml_tree(element)

        
class TestRun:
    def test_1_6(self, livesplit_1_6_lsspath):
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        # make this conditional on TestMetadata 
        element = root.find("Metadata").find("Run")
        Run.from_xml_tree(element)


class TestPlatform:
    def test_1_6(self, livesplit_1_6_lsspath):
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        # make this conditional on TestMetadata 
        element = root.find("Metadata").find("Platform")
        Platform.from_xml_tree(element)
            
class TestVariable:
    def test_1_6(self, livesplit_1_6_lsspath):
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        # make this conditional on TestMetadata 
        element = root.find("Metadata").find("Variable")
        Variable.from_xml_tree(element)


class TestAttempt:
    def test_1_6(self, livesplit_1_6_lsspath):
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        # maybe have a --verbose option that instantiates every possible Attempt model
        element = next(root.iter("Attempt"))
        Attempt.from_xml_tree(element)


class TestSegment:
    def test_1_6(self, livesplit_1_6_lsspath):
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        element = next(root.iter("Segment"))
        Segment.from_xml_tree(element)


class TestSplitTime:
    def test_1_6(self, livesplit_1_6_lsspath):
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        element = next(root.iter("SplitTime"))
        SplitTime.from_xml_tree(element)


class TestBestSegmentTime:
    def test_1_6(self, livesplit_1_6_lsspath):
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        element = next(root.iter("BestSegmentTime"))
        BestSegmentTime.from_xml_tree(element)


class TestTime:
    def test_1_6(self, livesplit_1_6_lsspath):
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        element = next(root.iter("Time"))
        Time.from_xml_tree(element)


class TestAutoSplitterSettings:
    def test_1_6(self, livesplit_1_6_lsspath):
        tree = ET.parse(livesplit_1_6_lsspath)
        root = tree.getroot()
        element = next(root.iter("AutoSplitterSettings"))
        AutoSplitterSettings.from_xml_tree(element)