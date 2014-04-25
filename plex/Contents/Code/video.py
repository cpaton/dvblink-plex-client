from xml.dom.minidom import parseString
from common import DVBLinkError
from common import DVBLinkStatus
from constants import *
from item import Item
from video_info import VideoInfo

class Video(Item):
    
    def __init__(self, xml_string):
        Item.__init__(self, xml_string)
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
                
    @property        
    def get_video_info(self):
        return self.video_info_
        
    def from_xml_(self, xml_string):
        video = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.video_info_ = VideoInfo(video.getElementsByTagName(VIDEO_INFO_ROOT_NODE)[0].toxml())
        except:
            return False            
        return True
        
class VideoList(list):

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
            
    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))        
        if not document.getElementsByTagName(VIDEO_ROOT_NODE):
            return False        
        for item_node in document.getElementsByTagName(VIDEO_ROOT_NODE):
            try:
                item = Video(item_node.toxml())
            except:
                pass
            else:
                self.append(item)      
        return True