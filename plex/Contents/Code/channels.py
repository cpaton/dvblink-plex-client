from xml.dom.minidom import Document, parseString
from common import DVBLinkError
from common import DVBLinkStatus
from common import string_to_bool
from constants import *

class ChannelType(object):

    CHANNEL_TV = 0
    CHANNEL_RADIO = 1
    CHANNEL_OTHER = 2
        
class ChannelsRequest(object):
    
    def to_xml(self):
        document = Document()
        channels = document.createElementNS(XMLDOC_NAMESPACE, CHANNELS_ROOT_NODE)
        channels.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(channels)      
        return document.toxml(encoding=XMLDOC_CODEPAGE)

class Channel(object):
    
    NUMBER_INVALID = -1
    SUBNUMBER_INVALID = 0
                  
    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
   
    @property
    def channel_id(self):
        return self.id_
    
    @property    
    def dvblink_channel_id(self):
        return self.dvblink_id_

    @property
    def channel_name(self):
        return self.name_
    
    @property
    def channel_number(self):
        return self.number_

    @property             
    def channel_subnumber(self):
        return self.subnumber_
    
    @property
    def channel_type(self):
        return self.channel_type_
        
    @property
    def is_child_locked(self):
        return self.is_child_locked_
        
    def from_xml_(self, xml_string):
        channel = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.id_ = str(channel.getElementsByTagName(CHANNEL_ID_NODE)[0].firstChild.data)
            self.dvblink_id_ = long(channel.getElementsByTagName(CHANNEL_DVBLINK_ID_NODE)[0].firstChild.data)
            self.name_ = channel.getElementsByTagName(CHANNEL_NAME_NODE)[0].firstChild.data
        except:
            return False        
        try:
            self.number_ = int(channel.getElementsByTagName(CHANNEL_NUMBER_NODE)[0].firstChild.data)
        except:
            self.number_ = self.NUMBER_INVALID                
        try:
            self.subnumber_ = int(channel.getElementsByTagName(CHANNEL_SUBNUMBER_NODE)[0].firstChild.data)
        except:
            self.subnumber_ = self.SUBNUMBER_INVALID
        try:
            self.channel_type_ = int(channel.getElementsByTagName(CHANNEL_TYPE_NODE)[0].firstChild.data)
        except:
            self.channel_type_ = ChannelType.CHANNEL_TV
        try:        
            self.is_child_locked_ = string_to_bool(channel.getElementsByTagName(CHANNEL_CHILD_LOCK_NODE)[0].firstChild.data)
        except:
            self.is_child_locked_ = False
        return True
        
class Channels(list):

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(STATUS_INVALID_DATA)
            
    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        for channel_node in document.getElementsByTagName(CHANNEL_ROOT_NODE):
            try:
                channel = Channel(channel_node.toxml())
            except:
                pass
            else:
                self.append(channel)        
        return True