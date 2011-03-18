"""
Storage Record tree.

Class for representing a storage record and generating xml.

Author: Henrik Thostrup Jensen <htj@ndgf.org>
Copyright: NorduNET / Nordic Data Grid Facility (2011)
"""

import time

from xml.etree import cElementTree as ET

import srelements



ISO_TIME_FORMAT   = "%Y-%m-%dT%H:%M:%S"
XML_HEADER        = '''<?xml version="1.0" encoding="UTF-8" ?>''' + "\n"



class StorageRecordTree:

    def __init__(self):
        self.record_id = None
        self.storage_system = None
        self.group = None
        self.measure_time = None
        self.valid_duration = None
        self.resource_consumption = None


    def generateTree(self):

        # utility function, very handy
        def setElement(parent, name, text):
            element = ET.SubElement(parent, name)
            element.text = str(text)


        assert self.record_id               is not None, 'No record id specified'
        assert self.storage_system          is not None, 'No storage system specified'
        assert self.measure_time            is not None, 'No meausure time specified'
        assert self.valid_duration          is not None, 'No valid duraction specified'
        assert self.resource_consumption    is not None, 'No resource consumption specified'

        sr = ET.Element(srelements.STORAGE_USAGE_RECORD)

        record_identity = ET.SubElement(sr, srelements.RECORD_IDENTITY)
        record_identity.set(srelements.RECORD_ID, self.record_id)
        record_identity.set(srelements.CREATE_TIME, time.strftime(ISO_TIME_FORMAT, time.gmtime()) + 'Z')

        setElement(sr, srelements.STORAGE_SYSTEM, self.storage_system)

        id_block = ET.SubElement(sr, srelements.SUBJECT_IDENTITY)
        if self.group is not None:
            setElement(id_block, srelements.GROUP, self.group)

        setElement(sr, srelements.MEASURE_TIME, self.measure_time)
        setElement(sr, srelements.RESOURCE_CAPACITY_USED, self.resource_consumption)

        return ET.ElementTree(sr)


    def writeXML(self, filename):

        tree = self.generateTree()
        f = file(filename, 'w')
        f.write(XML_HEADER)
        tree.write(f, encoding='utf-8')


