from xml.dom.minidom import Document, parseString
from programs import Program
from common import DVBLinkError
from common import DVBLinkStatus
from common import string_to_bool
from constants import *

class RecordingsRequest:
    
    def to_xml(self):
        document = Document()
        recordings = document.createElementNS(XMLDOC_NAMESPACE, RECORDINGS_ROOT_NODE)
        recordings.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(recordings)      
        return document.toxml(encoding=XMLDOC_CODEPAGE)        

class RecordingRemover:
    
    def __init__(self, recording_id):
        self.recording_id_ = recording_id
    
    def to_xml(self):
        document = Document()
        remover = document.createElementNS(XMLDOC_NAMESPACE, RECORDING_REMOVE_ROOT_NODE)
        remover.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(remover)
        # recording id
        id_node = document.createElement(RECORDING_ID_NODE)
        remover.appendChild(id_node)
        id_node.appendChild(document.createTextNode(self.recording_id_))            
        return document.toxml(encoding=XMLDOC_CODEPAGE)

class Recording:

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
   
    @property
    def recording_id(self):
        return self.id_
    
    @property    
    def schedule_id(self):
        return self.schedule_id_

    @property
    def channel_id(self):
        return self.channel_id_
    
    @property
    def is_active(self):
        return self.is_active_
    
    @property
    def is_conflicting(self):
        return self.is_conflicting_

    @property             
    def program(self):
        return self.program_
                
    def from_xml_(self, xml_string):
        recording = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.id_ = str(recording.getElementsByTagName(RECORDING_ID_NODE)[0].firstChild.data)
            self.schedule_id_ = str(recording.getElementsByTagName(RECORDING_SCHEDULE_ID_NODE)[0].firstChild.data)
            self.channel_id_ = str(recording.getElementsByTagName(RECORDING_CHANNEL_ID_NODE)[0].firstChild.data)
        except:
            return False        
        try:
            self.is_active_ = string_to_bool(recording.getElementsByTagName(RECORDING_IS_ACTIVE_NODE)[0].firstChild.data)
        except:
            self.is_active_ = False
        try:
            self.is_conflicting_ = string_to_bool(recording.getElementsByTagName(RECORDING_IS_CONFLICT_NODE)[0].firstChild.data)
        except:
            self.is_conflicting_ = False
        try:
            self.program_ = Program(recording.toxml())
        except:
            self.program_ = None
        return True
        
class Recordings(list):

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
            
    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        for recording_node in document.getElementsByTagName(RECORDING_ROOT_NODE):
            try:
                recording = Recording(recording_node.toxml())
            except:
                pass
            else:
                self.append(recording)        
        return True