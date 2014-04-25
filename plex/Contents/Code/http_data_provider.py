import httplib
import urllib
import socket
import base64
import channels
import programs
import streamer
import recordings
import schedules
import stream_info
import parental_lock
import helper
import object as media_object
from common import DVBLinkError
from common import DVBLinkStatus
from constants import *
from xml.dom.minidom import parseString

class HttpDataProvider(object):

    URL_SUFFIX_ = "/mobile/"
    METHOD_POST_ = "POST"
    CMD_PARAM_ = "command"
    XML_PARAM_ = "xml_param"
    REQUEST_TIMEOUT_SEC_ = 60
    STATUS_UNAUTHORISED_ = 401

    GET_CHANNELS_CMD_ = "get_channels"
    GET_STREAM_INFO_CMD_ = "get_stream_info"
    PLAY_CHANNEL_CMD_ = "play_channel"
    STOP_CHANNEL_CMD_ = "stop_channel"
    SEARCH_EPG_CMD_ = "search_epg"
    GET_RECORDINGS_CMD_ = "get_recordings"
    GET_SCHEDULES_CMD_ = "get_schedules"
    ADD_SCHEDULE_CMD_ = "add_schedule"
    UPDATE_SCHEDULE_CMD_ = "update_schedule"
    REMOVE_SCHEDULE_CMD_ = "remove_schedule"
    REMOVE_RECORDING_CMD_ = "remove_recording"
    SET_PARENTAL_LOCK_CMD_ = "set_parental_lock"
    GET_PARENTAL_STATUS_CMD_ = "get_parental_status"
    GET_OBJECTS_CMD_ = "get_object"
    REMOVE_OBJECT_CMD_ = "remove_object"
    STOP_RECORDING_CMD_ = "stop_recording"
   
    def __init__(self, address, port, user_name, password):
        self.address_ = address
        self.port_ = port
        self.user_name_ = user_name
        self.password_ = password
        socket.setdefaulttimeout(self.REQUEST_TIMEOUT_SEC_)
             
    def get_channels(self):
        request = channels.ChannelsRequest()
        xml_channels = self.get_data_(self.GET_CHANNELS_CMD_, request.to_xml())
        if xml_channels == None or len(xml_channels) == 0:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
        return channels.Channels(xml_channels)
        
    def get_stream_info(self, request_stream_info):
        xml_info = self.get_data_(self.GET_STREAM_INFO_CMD_, request_stream_info.to_xml())
        if xml_info == None or len(xml_info) == 0:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
        return stream_info.StreamInfoList(xml_info)
    
    def search_epg(self, epg_searcher):        
        xml_programs = self.get_data_(self.SEARCH_EPG_CMD_, epg_searcher.to_xml())
        if xml_programs == None or len(xml_programs) == 0:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
        return programs.ChannelsIdWithPrograms(xml_programs)
        
    def play_channel(self, request_stream):
        xml_streamer = self.get_data_(self.PLAY_CHANNEL_CMD_, request_stream.to_xml())
        if xml_streamer == None or len(xml_streamer) == 0:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
        return streamer.Streamer(xml_streamer)
        
    def stop_channel(self, stop_stream):
        self.get_data_(self.STOP_CHANNEL_CMD_, stop_stream.to_xml())
        return True
        
    def get_recordings(self):
        request = recordings.RecordingsRequest()
        xml_recordings = self.get_data_(self.GET_RECORDINGS_CMD_, request.to_xml())
        if xml_recordings == None or len(xml_recordings) == 0:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)        
        return recordings.Recordings(xml_recordings)

    def get_schedules(self):
        request = schedules.SchedulesRequest()
        xml_schedules = self.get_data_(self.GET_SCHEDULES_CMD_, request.to_xml())
        if xml_schedules == None or len(xml_schedules) == 0:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)        
        return schedules.Schedules(xml_schedules)
        
    def add_schedule(self, schedule):
        self.get_data_(self.ADD_SCHEDULE_CMD_, schedule.to_xml())
        return True

    def update_schedule(self, schedule_updater):
        self.get_data_(self.UPDATE_SCHEDULE_CMD_, schedule_updater.to_xml())
        return True
    
    def remove_schedule(self, schedule_remover):
        self.get_data_(self.REMOVE_SCHEDULE_CMD_, schedule_remover.to_xml())
        return True

    def remove_recording(self, recording_remover):
        self.get_data_(self.REMOVE_RECORDING_CMD_, recording_remover.to_xml())
        return True        
        
    def get_object(self, object_requester):
        xml_objects = self.get_data_(self.GET_OBJECTS_CMD_, object_requester.to_xml())
        if xml_objects == None or len(xml_objects) == 0:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)        
        return media_object.Object(xml_objects)
    
    def remove_object(self, object_remover):
        self.get_data_(self.REMOVE_OBJECT_CMD_, object_remover.to_xml())
        return True
        
    def stop_recording(self, stop_recording):
        self.get_data_(self.STOP_RECORDING_CMD_, stop_recording.to_xml())
        return True
    
    def set_parental_lock(self, parental_lock):
        self.get_data_(self.SET_PARENTAL_LOCK_CMD_, parental_lock.to_xml())
        return True
    
    def get_data_(self, command, xml_string):
        response = self.post_request_(command, xml_string)
        if len(response) == 0:
            helper.log_error('HttpDataProvider.get_data_. Response is empty')
            raise DVBLinkError(DVBLinkStatus.STATUS_CONNECTION_ERROR)
        return self.get_xml_string_(response)
    
    def post_request_(self, command, xml_string):
        try:
            auth_string = "Basic " + base64.b64encode(self.user_name_ + ":" + self.password_)
            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain",
                       "Authorization": auth_string}
            connection = httplib.HTTPConnection(self.address_ + ":" + str(self.port_))
            post_request = urllib.urlencode({self.CMD_PARAM_: command, self.XML_PARAM_: xml_string})
            connection.request(self.METHOD_POST_, self.URL_SUFFIX_, post_request, headers)
            response = connection.getresponse()
            if self.STATUS_UNAUTHORISED_ == response.status:
                helper.log_error('HttpDataProvider.post_request_. Unauthorized error')
                raise DVBLinkError(DVBLinkStatus.STATUS_UNAUTHORISED)
            data = response.read()
            connection.close()
            return data
        except socket.error, error:
            helper.log_error('HttpDataProvider.post_request_. Socket error')
            raise DVBLinkError(DVBLinkStatus.STATUS_CONNECTION_ERROR)

    def get_xml_string_(self, response):
        status = DVBLinkStatus.STATUS_INVALID_DATA
        try:
            document = parseString(response)
            status = int(document.getElementsByTagName(STATUS_CODE_NODE)[0].firstChild.data)
        except Exception, error:
            helper.log_error('HttpDataProvider.get_xml_string_. %s' % str(error))
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
        if status != DVBLinkStatus.STATUS_OK:
            raise DVBLinkError(status)
        try:
            return document.getElementsByTagName(XML_RESULT_NODE)[0].firstChild.data
        except:
            pass
        return None