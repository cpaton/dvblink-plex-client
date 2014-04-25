from xml.dom.minidom import parseString
from common import DVBLinkError
from common import DVBLinkStatus
from common import string_to_bool
from constants import *

class ItemType(object):
    
    ITEM_UNKNOWN = -1
    ITEM_RECORDED_TV = 0
    ITEM_VIDEO = 1
    ITEM_AUDIO = 2
    ITEM_IMAGE = 3
      
class Item(object):

    def __init__(self, xml_string):
        if self.from_xml__(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
   
    @property
    def object_id(self):
        return self.object_id_
    
    @property    
    def parent_id(self):
        return self.parent_id_

    @property
    def url(self):
        return self.url_
    
    @property
    def thumbnail(self):
        return self.thumbnail_

    @property             
    def can_be_deleted(self):
        return self.can_be_deleted_
    
    @property             
    def size(self):
        return self.size_
        
    @property             
    def creation_time(self):
        return self.creation_time_
                
    def from_xml__(self, xml_string):
        item = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.object_id_ = str(item.getElementsByTagName(ITEM_OBJECT_ID_NODE)[0].firstChild.data)
            self.parent_id_ = str(item.getElementsByTagName(ITEM_PARENT_ID_NODE)[0].firstChild.data)
        except:
            return False
        try:
            self.url_ = str(item.getElementsByTagName(ITEM_URL_NODE)[0].firstChild.data)
        except:
            self.url_ = ""
        try:
            self.thumbnail_ = str(item.getElementsByTagName(ITEM_THUMBNAIL_NODE)[0].firstChild.data)
        except:
            self.thumbnail_ = ""
        try:
            self.can_be_deleted_ = string_to_bool(item.getElementsByTagName(ITEM_CAN_BE_DELETED_NODE)[0].firstChild.data)
        except:
            self.can_be_deleted_ = False
        try:
            self.size_ = int(item.getElementsByTagName(ITEM_SIZE_NODE)[0].firstChild.data)
        except:
            self.size_ = 0
        try:
            self.creation_time_ = int(item.getElementsByTagName(ITEM_CREATION_TIME_NODE)[0].firstChild.data)
        except:
            self.creation_time_ = 0
        return True
        
class ItemList(list):

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
            
    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        for item_node in document.getElementsByTagName(ITEM_ROOT_NODE):
            try:
                item = Item(item_node.toxml())
            except:
                pass
            else:
                self.append(item)        
        return True