from xml.dom.minidom import Document, parseString
from common import DVBLinkError
from common import DVBLinkStatus
from item import ItemType
from constants import *

class ContainerType(object):
    
    CONTAINER_UNKNOWN = -1
    CONTAINER_SOURCE = 0
    CONTAINER_TYPE = 1
    CONTAINER_CATEGORY = 2
    CONTAINER_CATEGORY_SORT = 3
    CONTAINER_CATEGORY_GROUP = 4
    CONTAINER_GROUP = 5

class Container(object):
    
    OBJECT_COUNT_UNKNOWN = -1

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
   
    @property
    def object_id(self):
        return self.object_id_
    
    @property    
    def parent_id(self):
        return self.parent_id_
        
    @property    
    def source_id(self):
        return self.source_id_

    @property
    def name(self):
        return self.name_
    
    @property
    def description(self):
        return self.description_
  
    @property             
    def logotype(self):
        return self.logotype_
        
    @property
    def type(self):
        return self.type_
        
    @property
    def content_type(self):
        return self.content_type_
        
    @property
    def total_count(self):
        return self.total_count_

    def from_xml_(self, xml_string):
        container = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.object_id_ = str(container.getElementsByTagName(CONTAINER_OBJECT_ID_NODE)[0].firstChild.data)
        except:
            return False               
        try:
            self.parent_id_ = str(container.getElementsByTagName(CONTAINER_PARENT_ID_NODE)[0].firstChild.data)
        except:
            self.parent_id_ = None
        try:
            self.source_id_ = str(container.getElementsByTagName(CONTAINER_SOURCE_ID_NODE)[0].firstChild.data)
        except:
            self.source_id_ = None
        try:
            self.name_ = container.getElementsByTagName(CONTAINER_NAME_NODE)[0].firstChild.data
        except:
            self.name_ = ""
        try:
            self.description_ = container.getElementsByTagName(CONTAINER_DESCRIPTION_NODE)[0].firstChild.data
        except:
            self.description_ = ""
        try:
            self.logotype_ = str(container.getElementsByTagName(CONTAINER_LOGO_NODE)[0].firstChild.data)
        except:
            self.logotype_ = ""
        try:
            self.type_ = int(container.getElementsByTagName(CONTAINER_TYPE_NODE)[0].firstChild.data)
        except:
            self.type_ = ContainerType.CONTAINER_UNKNOWN
        try:
            self.content_type_ = int(container.getElementsByTagName(CONTAINER_CONTENT_TYPE_NODE)[0].firstChild.data)
        except:
            self.content_type_ = ItemType.ITEM_UNKNOWN
        try:
            self.total_count_ = int(container.getElementsByTagName(CONTAINER_TOTAL_COUNT_NODE)[0].firstChild.data)
        except:
            self.total_count_ = self.OBJECT_COUNT_UNKNOWN
        return True
     
class ContainerList(list):

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
            
    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        for container_node in document.getElementsByTagName(CONTAINER_ROOT_NODE):
            try:
                container = Container(container_node.toxml())
            except:
                pass
            else:
                self.append(container)        
        return True       