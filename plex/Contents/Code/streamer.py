from xml.dom.minidom import Document, parseString
from common import DVBLinkError
from common import DVBLinkStatus
from constants import *

class RequestStream:

    RAW_HTTP_TYPE_ = "raw_http"

    def __init__(self, channel_dvblink_id, client_id, server_address):
        self.channel_dvblink_id_ = channel_dvblink_id
        self.client_id_ = client_id
        self.server_address_ = server_address
        self.stream_type_ = self.RAW_HTTP_TYPE_

    def to_xml(self):
        document = Document()
        request_stream = document.createElementNS(XMLDOC_NAMESPACE, STREAMER_ROOT_NODE)
        request_stream.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(request_stream)
        
        if self.channel_dvblink_id_ != None:
            channel_id = document.createElement(STREAMER_CHANNEL_ID_NODE)
            request_stream.appendChild(channel_id)
            channel_id.appendChild(document.createTextNode(str(self.channel_dvblink_id_)))
        if self.client_id_ != None:
            client_id = document.createElement(STREAMER_CLIENT_ID_NODE)
            request_stream.appendChild(client_id)
            client_id.appendChild(document.createTextNode(str(self.client_id_)))
        if self.server_address_ != None:
            address = document.createElement(STREAMER_SERVER_ADDRESS_NODE)
            request_stream.appendChild(address)
            address.appendChild(document.createTextNode(str(self.server_address_)))
        if self.stream_type_ != None:
            stream_type = document.createElement(STREAMER_STREAM_TYPE_NODE)
            request_stream.appendChild(stream_type)
            stream_type.appendChild(document.createTextNode(str(self.stream_type_)))
        return document.toxml(encoding=XMLDOC_CODEPAGE)
        
class Streamer:

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
   
    @property
    def get_channel_handle(self):
        return self.channel_handle_
    
    @property
    def get_url(self):
        return self.url_
               
    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.channel_handle_ = long(document.getElementsByTagName(STREAMER_CHANNEL_HANDLE_NODE)[0].firstChild.data)
            self.url_ = document.getElementsByTagName(STREAMER_URL_NODE)[0].firstChild.data
        except:
            return False
        return True

class StopStream:

    def __init__(self, **kwargs):
        kwargs.setdefault(STREAMER_CHANNEL_HANDLE_NODE, None)
        kwargs.setdefault(STREAMER_CLIENT_ID_NODE, None)
        
        self.channel_handle_ = kwargs[STREAMER_CHANNEL_HANDLE_NODE]
        self.client_id_ = kwargs[STREAMER_CLIENT_ID_NODE]
    
    def to_xml(self):
        document = Document()
        stop_stream = document.createElementNS(XMLDOC_NAMESPACE, STREAMER_STOP_ROOT_NODE)
        stop_stream.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(stop_stream)
        
        if self.channel_handle_ != None:
            channel_handle = document.createElement(STREAMER_CHANNEL_HANDLE_NODE)
            stop_stream.appendChild(channel_handle)
            channel_handle.appendChild(document.createTextNode(str(self.channel_handle_)))
        elif self.client_id_ != None:
            client_id = document.createElement(STREAMER_CLIENT_ID_NODE)
            stop_stream.appendChild(client_id)
            client_id.appendChild(document.createTextNode(str(self.client_id_)))
        return document.toxml(encoding=XMLDOC_CODEPAGE)