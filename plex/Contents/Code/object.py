from xml.dom.minidom import Document, parseString
from constants import *
from item import ItemType
from container import ContainerList
from video import VideoList
from recorded_tv import RecordedTVList

class ObjectType(object):
    
    OBJECT_UNKNOWN = -1
    OBJECT_CONTAINER = 0
    OBJECT_ITEM = 1

class Object(object):
    
    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
    
    @property
    def containers(self):
        return self.containers_
        
    @property
    def items(self):
        return self.items_
        
    @property
    def actual_count(self):
        return self.actual_count_
        
    @property
    def total_count(self):
        return self.total_count_
        
    def from_xml_(self, xml_string):  
        objects = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.containers_ = ContainerList(objects.getElementsByTagName(CONTAINERS_ROOT_NODE)[0].toxml())
        except:
            self.containers_ = None
        try:
            self.items_ = self.get_items_(objects.getElementsByTagName(ITEMS_ROOT_NODE)[0].toxml())
        except:
            self.items_ = None
        try:
            self.actual_count_ = int(objects.getElementsByTagName(OBJECT_ACTUAL_COUNT_NODE)[0].firstChild.data)
        except:
            self.actual_count_ = 0
        try:
            self.total_count_ = int(objects.getElementsByTagName(OBJECT_TOTAL_COUNT_NODE)[0].firstChild.data)
        except:
            self.total_count_ = 0
        return True

    def get_items_(self, xml_string):
        try:
            return VideoList(xml_string)
        except:
            try:
                return RecordedTVList(xml_string)
            except:
                pass
        return None
        
class ObjectRequester(object):
    
    OBJECT_ROOT_ID = ""
    OBJECT_START_POSITION = 0
    OBJECT_COUNT_ALL = -1
      
    def __init__(self, **kwargs):
        kwargs.setdefault(OBJECT_REQUESTER_OBJECT_ID_NODE, self.OBJECT_ROOT_ID)
        kwargs.setdefault(OBJECT_REQUESTER_SERVER_ADDR_NODE, None)
        kwargs.setdefault(OBJECT_REQUESTER_OBJECT_TYPE_NODE, ObjectType.OBJECT_UNKNOWN)        
        kwargs.setdefault(OBJECT_REQUESTER_ITEM_TYPE_NODE, ItemType.ITEM_UNKNOWN)
        kwargs.setdefault(OBJECT_REQUESTER_POSITION_NODE, self.OBJECT_START_POSITION)
        kwargs.setdefault(OBJECT_REQUESTER_COUNT_NODE, self.OBJECT_COUNT_ALL)
        kwargs.setdefault(OBJECT_REQUESTER_TYPE_NODE, True)

        self.object_id_ = kwargs[OBJECT_REQUESTER_OBJECT_ID_NODE]
        self.server_address_ = kwargs[OBJECT_REQUESTER_SERVER_ADDR_NODE]
        self.object_type_ = kwargs[OBJECT_REQUESTER_OBJECT_TYPE_NODE]
        self.item_type_ = kwargs[OBJECT_REQUESTER_ITEM_TYPE_NODE]
        self.start_position_ = kwargs[OBJECT_REQUESTER_POSITION_NODE]
        self.requested_count_ = kwargs[OBJECT_REQUESTER_COUNT_NODE]
        self.is_children_request_ = kwargs[OBJECT_REQUESTER_TYPE_NODE]
    
    def to_xml(self):
        document = Document()
        object_requester = document.createElementNS(XMLDOC_NAMESPACE, OBJECT_REQUESTER_ROOT_NODE)
        object_requester.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(object_requester)        
        
        object_id = document.createElement(OBJECT_REQUESTER_OBJECT_ID_NODE)
        object_requester.appendChild(object_id)
        object_id.appendChild(document.createTextNode(str(self.object_id_)))                 
        
        if self.server_address_ != None:
            server_address = document.createElement(OBJECT_REQUESTER_SERVER_ADDR_NODE)
            object_requester.appendChild(server_address)
            server_address.appendChild(document.createTextNode(str(self.server_address_)))
            
        object_type = document.createElement(OBJECT_REQUESTER_OBJECT_TYPE_NODE)
        object_requester.appendChild(object_type)
        object_type.appendChild(document.createTextNode(str(self.object_type_)))
        
        item_type = document.createElement(OBJECT_REQUESTER_ITEM_TYPE_NODE)
        object_requester.appendChild(item_type)
        item_type.appendChild(document.createTextNode(str(self.item_type_)))
        
        start_position = document.createElement(OBJECT_REQUESTER_POSITION_NODE)
        object_requester.appendChild(start_position)
        start_position.appendChild(document.createTextNode(str(self.start_position_)))
        
        requested_count = document.createElement(OBJECT_REQUESTER_COUNT_NODE)
        object_requester.appendChild(requested_count)
        requested_count.appendChild(document.createTextNode(str(self.requested_count_)))
            
        if self.is_children_request_:
            is_children_request = document.createElement(OBJECT_REQUESTER_TYPE_NODE)
            object_requester.appendChild(is_children_request)
            is_children_request.appendChild(document.createTextNode(XMLNODE_VALUE_TRUE))
                     
        return document.toxml(encoding=XMLDOC_CODEPAGE)
        
class ObjectRemover(object):
    
    def __init__(self, object_id):
        self.object_id_ = object_id
    
    def to_xml(self):
        document = Document()
        remover = document.createElementNS(XMLDOC_NAMESPACE, OBJECT_REMOVER_ROOT_NODE)
        remover.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(remover)
        # object id
        id_node = document.createElement(OBJECT_REMOVER_OBJECT_ID_NODE)
        remover.appendChild(id_node)
        id_node.appendChild(document.createTextNode(self.object_id_))            
        return document.toxml(encoding=XMLDOC_CODEPAGE)        
