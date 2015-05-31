from xml.dom.minidom import Document, parseString
from common import DVBLinkError
from common import DVBLinkStatus
from constants import *
from item import Item
from video_info import VideoInfo

class RecordedTVState(object):

    RTVS_IN_PROGRESS = 0
    RTVS_ERROR = 1
    RTVS_FORCED_TO_COMPLETION = 2
    RTVS_COMPLETED = 3

class StopRecording(object):

    def __init__(self, object_id):
        self.object_id_ = object_id

    def to_xml(self):
        document = Document()
        remover = document.createElementNS(XMLDOC_NAMESPACE, STOP_RECORDING_ROOT_NODE)
        remover.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(remover)
        # object id
        id_node = document.createElement(STOP_RECORDING_ID_NODE)
        remover.appendChild(id_node)
        id_node.appendChild(document.createTextNode(self.object_id_))
        return document.toxml(encoding=XMLDOC_CODEPAGE)

class RecordedTV(Item):

    def __init__(self, xml_string):
        Item.__init__(self, xml_string)
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)

    @property
    def video_info(self):
        return self.video_info_

    @property
    def channel_name(self):
        return self.channel_name_

    @property
    def channel_number(self):
        return self.channel_number_

    @property
    def channel_subnumber(self):
        return self.channel_subnumber_

    @property
    def recording_title(self):
        if (self.video_info.episode_number == 0) or (self.video_info.season_number == 0):
            return '{0} - {1}'.format(self.video_info.name, self.video_info.subname)
        else:
            return '{0} - S{1}E{2} - {3}'.format(self.video_info.name, str(self.video_info.season_number).zfill(2), str(self.video_info.episode_number).zfill(2), self.video_info.subname)
            
    @property
    def state(self):
        return self.state_

    def from_xml_(self, xml_string):
        recorded_tv = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.video_info_ = VideoInfo(recorded_tv.getElementsByTagName(VIDEO_INFO_ROOT_NODE)[0].toxml())
        except:
            return False
        try:
            self.channel_name_ = recorded_tv.getElementsByTagName(RECORDED_TV_CHANNEL_NAME_NODE)[0].firstChild.data
        except:
            self.channel_name_ = None
        try:
            self.channel_number_ = int(recorded_tv.getElementsByTagName(RECORDED_TV_CHANNEL_NUMBER_NODE)[0].firstChild.data)
        except:
            self.channel_number_ = 0
        try:
            self.channel_subnumber_ = int(recorded_tv.getElementsByTagName(RECORDED_TV_CHANNEL_SUBNUMBER_NODE)[0].firstChild.data)
        except:
            self.channel_subnumber_ = 0
        try:
            self.state_ = int(recorded_tv.getElementsByTagName(RECORDED_TV_STATE_NODE)[0].firstChild.data)
        except:
            self.state_ = RecordedTVState.RTVS_COMPLETED
        return True

class RecordedTVList(list):

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)

    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        if not document.getElementsByTagName(RECORDED_TV_ROOT_NODE):
            return False
        for item_node in document.getElementsByTagName(RECORDED_TV_ROOT_NODE):
            try:
                item = RecordedTV(item_node.toxml())
            except:
                pass
            else:
                self.append(item)
        return True
