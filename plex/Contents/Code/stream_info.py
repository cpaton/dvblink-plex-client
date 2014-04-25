from xml.dom.minidom import Document, parseString
from common import DVBLinkError
from common import DVBLinkStatus
from constants import *

class StreamInfoRequest(object):
    
    def __init__(self, address, client_id, channels_ids):
        self.address_ = address
        self.client_id_ = client_id
        self.channels_ids_ = channels_ids
    
    def to_xml(self):
        document = Document()
        stream_info = document.createElementNS(XMLDOC_NAMESPACE, STREAM_INFO_ROOT_NODE)
        stream_info.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(stream_info)        

        address_node = document.createElement(STREAM_INFO_SERVER_ADDRESS_NODE)
        stream_info.appendChild(address_node)
        address_node.appendChild(document.createTextNode(self.address_))                    
        
        client_id_node = document.createElement(STREAM_INFO_CLIENT_ID_NODE)
        stream_info.appendChild(client_id_node)
        client_id_node.appendChild(document.createTextNode(self.client_id_))
   
        channels_ids = document.createElement(STREAM_INFO_CHANNELS_IDS_NODE)
        stream_info.appendChild(channels_ids)
        for id in self.channels_ids_:
            id_node = document.createElement(STREAM_INFO_CHANNEL_ID_NODE)
            channels_ids.appendChild(id_node)
            id_node.appendChild(document.createTextNode(str(id)))
        return document.toxml(encoding=XMLDOC_CODEPAGE)
        
class StreamInfo(object):

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)

    @property
    def dvblink_channel_id(self):
        return self.dvblink_id_
        
    @property
    def channel_url(self):
        return self.channel_url_

    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.dvblink_id_ = long(document.getElementsByTagName(STREAM_INFO_CHANNEL_ID_NODE)[0].firstChild.data)
            self.channel_url_ = document.getElementsByTagName(STREAM_INFO_CHANNEL_URL_NODE)[0].firstChild.data
        except:
            return False
        return True        

class StreamInfoList(list):

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(STATUS_INVALID_DATA)
            
    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        for stream_info_node in document.getElementsByTagName(STREAM_INFO_CHANNEL_ROOT_NODE):
            try:
                channel = StreamInfo(stream_info_node.toxml())
            except:
                pass
            else:
                self.append(channel)        
        return True