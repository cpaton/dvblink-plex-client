from xml.dom.minidom import Document, parseString
from common import DVBLinkError
from common import DVBLinkStatus
from common import string_to_bool
from constants import *

class ParentalLock(object):

    def __init__(self, **kwargs):
        kwargs.setdefault(PARENTAL_LOCK_CLIENT_ID_NODE, None)
        kwargs.setdefault(PARENTAL_LOCK_IS_ENABLE_NODE, False)
        kwargs.setdefault(PARENTAL_LOCK_CODE_NODE, None)        

        self.client_id_ = kwargs[PARENTAL_LOCK_CLIENT_ID_NODE]
        self.is_enable_ = kwargs[PARENTAL_LOCK_IS_ENABLE_NODE]
        self.lock_code_ = kwargs[PARENTAL_LOCK_CODE_NODE]        
    
    def to_xml(self):
        document = Document()
        parental_lock = document.createElementNS(XMLDOC_NAMESPACE, PARENTAL_LOCK_ROOT_NODE)
        parental_lock.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(parental_lock)        
        if self.is_enable_:
            is_enable = document.createElement(PARENTAL_LOCK_IS_ENABLE_NODE)
            parental_lock.appendChild(is_enable)
            is_enable.appendChild(document.createTextNode(XMLNODE_VALUE_TRUE))
        
        if self.lock_code_ != None:
            lock_code = document.createElement(PARENTAL_LOCK_CODE_NODE)
            parental_lock.appendChild(lock_code)
            lock_code.appendChild(document.createTextNode(self.lock_code_.decode(XMLDOC_CODEPAGE)))
            
        if self.client_id_ != None:
            client_id = document.createElement(PARENTAL_LOCK_CLIENT_ID_NODE)
            parental_lock.appendChild(client_id)
            client_id.appendChild(document.createTextNode(self.client_id_))
        
        return document.toxml(encoding=XMLDOC_CODEPAGE)
        
class ParentalStatus(object):

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
   
    @property
    def is_enabled(self):
        return self.is_enabled_
        
    def from_xml_(self, xml_string):
        status = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:        
            self.is_enabled_ = string_to_bool(status.getElementsByTagName(PARENTAL_STATUS_IS_ENABLED_NODE)[0].firstChild.data)
        except:
            return False
        return True