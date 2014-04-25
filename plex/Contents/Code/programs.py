from xml.dom.minidom import parseString
from common import DVBLinkError
from common import DVBLinkStatus
from common import string_to_bool
from constants import *
from video_info import VideoInfo

class Program(VideoInfo):
    def __init__(self, xml_string):
        VideoInfo.__init__(self, xml_string)
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)

    @property        
    def program_id(self):
        return self.program_id_

    @property
    def is_series(self):
        return self.is_series_
    
    @property
    def is_record(self):
        return self.is_record_
    
    @property
    def is_repeat_record(self):
        return self.is_repeat_record_
    
    def from_xml_(self, xml_string):
        program = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.program_id_ = str(program.getElementsByTagName(PROGRAM_ID_NODE)[0].firstChild.data)
        except:
            self.program_id_ = None        
        try:
            self.is_series_ = string_to_bool(program.getElementsByTagName(PROGRAM_IS_SERIES_NODE)[0].firstChild.data)
        except:
            self.is_series_ = False
        try:
            self.is_record_ = string_to_bool(program.getElementsByTagName(PROGRAM_IS_RECORD_NODE)[0].firstChild.data)
        except:
            self.is_record_ = False
        try:    
            self.is_repeat_record_ = string_to_bool(program.getElementsByTagName(PROGRAM_IS_REPEAT_RECORD_NODE)[0].firstChild.data)
        except:
            self.is_repeat_record_ = False

        return True
               
class ChannelsIdWithPrograms(dict):   
    
    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
            
    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        for channel_epg in document.getElementsByTagName(SEARCHING_CHANNEL_EPG_NODE):
            try:            
                channel_id = str(channel_epg.getElementsByTagName(PROGRAM_CHANNEL_ID_NODE)[0].firstChild.data)
                if channel_id != None:
                    programs = []
                    for program_node in channel_epg.getElementsByTagName(EPG_PROGRAM):
                        try:          
                            program = Program(program_node.toxml())
                        except:
                            pass
                        else:
                            programs.append(program)
                    self[channel_id] = programs                    
            except:
                pass
        return True