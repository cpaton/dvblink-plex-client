from xml.dom.minidom import Document, parseString
from programs import Program
from common import DVBLinkError
from common import DVBLinkStatus
from common import string_to_bool
from constants import *

class SchedulesRequest:
    
    def to_xml(self):
        document = Document()
        schedules = document.createElementNS(XMLDOC_NAMESPACE, SCHEDULES_ROOT_NODE)
        schedules.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(schedules)      
        return document.toxml(encoding=XMLDOC_CODEPAGE)
        
class ScheduleRemover:
    
    def __init__(self, schedule_id):
        self.schedule_id_ = schedule_id
    
    def to_xml(self):
        document = Document()
        remover = document.createElementNS(XMLDOC_NAMESPACE, SCHEDULE_REMOVE_ROOT_NODE)
        remover.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(remover)
        # schedule id
        id_node = document.createElement(SCHEDULE_ID_NODE)
        remover.appendChild(id_node)
        id_node.appendChild(document.createTextNode(self.schedule_id_))            
        return document.toxml(encoding=XMLDOC_CODEPAGE)

class ScheduleUpdater:
    def __init__(self, **kwargs):
        kwargs.setdefault(SCHEDULE_ID_NODE, None)
        kwargs.setdefault(SCHEDULE_NEW_ONLY_NODE, False)
        kwargs.setdefault(SCHEDULE_SERIES_ANYTIME_NODE, False)
        kwargs.setdefault(SCHEDULE_REC_TO_KEEP_NODE, None)

        self.schedule_id_ = kwargs[SCHEDULE_ID_NODE]
        self.is_new_only_ = kwargs[SCHEDULE_NEW_ONLY_NODE]
        self.is_record_series_anytime_ = kwargs[SCHEDULE_SERIES_ANYTIME_NODE]
        self.recordings_to_keep_ = kwargs[SCHEDULE_REC_TO_KEEP_NODE]

    def to_xml(self):
        document = Document()
        schedule = document.createElementNS(XMLDOC_NAMESPACE, SCHEDULE_UPDATE_ROOT_NODE)
        schedule.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(schedule)
        if self.schedule_id_ != None:
            schedule_id_node = document.createElement(SCHEDULE_ID_NODE)
            schedule.appendChild(schedule_id_node)
            schedule_id_node.appendChild(document.createTextNode(self.schedule_id_))
        if self.is_new_only_:
            is_new_only_node = document.createElement(SCHEDULE_NEW_ONLY_NODE)
            schedule.appendChild(is_new_only_node)
            is_new_only_node.appendChild(document.createTextNode(XMLNODE_VALUE_TRUE))
        if self.is_record_series_anytime_:
            is_record_series_anytime_node = document.createElement(SCHEDULE_SERIES_ANYTIME_NODE)
            schedule.appendChild(is_record_series_anytime_node)
            is_record_series_anytime_node.appendChild(document.createTextNode(XMLNODE_VALUE_TRUE))
        if self.recordings_to_keep_ != None:
            recordings_to_keep_node = document.createElement(SCHEDULE_REC_TO_KEEP_NODE)
            schedule.appendChild(recordings_to_keep_node)
            recordings_to_keep_node.appendChild(document.createTextNode(str(self.recordings_to_keep_)))            
        return document.toxml(encoding=XMLDOC_CODEPAGE)

class Schedule:

    def __init__(self, **kwargs):
        kwargs.setdefault(SCHEDULE_ID_NODE, None)
        kwargs.setdefault(SCHEDULE_USER_PARAM_NODE, None)
        kwargs.setdefault(SCHEDULE_FORCE_ADD_NODE, False)
        kwargs.setdefault(SCHEDULE_BY_EPG_ROOT_NODE, None)
        kwargs.setdefault(SCHEDULE_MANUAL_ROOT_NODE, None)

        self.schedule_id_ = kwargs[SCHEDULE_ID_NODE]
        self.user_param_ = kwargs[SCHEDULE_USER_PARAM_NODE]
        self.force_add_ = kwargs[SCHEDULE_FORCE_ADD_NODE]
        self.by_epg_ = kwargs[SCHEDULE_BY_EPG_ROOT_NODE]
        self.manual_ = kwargs[SCHEDULE_MANUAL_ROOT_NODE]

    @property
    def id(self):
        return self.schedule_id_
    
    @property
    def title(self):
        if self.is_by_epg:
            return self.by_epg_.title
        return self.manual_.title
        
    @property
    def start_time(self):
        if self.is_by_epg:
            return self.by_epg_.start_time
        return self.manual_.start_time
        
    @property
    def duration(self):
        if self.is_by_epg:
            return self.by_epg_.duration
        return self.manual_.duration
        
    @property
    def channel_id(self):
        if self.is_by_epg:
            return self.by_epg_.channel_id
        return self.manual_.channel_id
    
    @property
    def user_param(self):
        return self.user_param_
    
    @property
    def force_add(self):
        return self.force_add_
    
    @property
    def is_repeat(self):
        if self.is_by_epg:
            return self.by_epg_.is_repeat
        return self.manual_.day_mask != ManualSchedule.DAY_MASK_ONCE
    
    @property
    def is_new_only(self):
        if self.is_by_epg:
            return self.by_epg_.is_new_only
        return None
        
    @property
    def is_record_series_anytime(self):
        if self.is_by_epg:
            return self.by_epg_.is_record_series_anytime
        return None
    
    @property    
    def recordings_to_keep(self):
        if self.is_by_epg:
            return self.by_epg_.recordings_to_keep
        return self.manual_.recordings_to_keep
        
    @property
    def is_by_epg(self):
        return None != self.by_epg_ and None != self.by_epg_.program_id
    
    @property
    def is_manual(self):
        return None != self.manual_ and None != self.manual_.start_time and None != self.manual_.duration
               
    def to_xml(self):
        document = Document()
        schedule = document.createElementNS(XMLDOC_NAMESPACE, SCHEDULE_ROOT_NODE)
        schedule.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(schedule)
        # schedule id
        if self.schedule_id_ != None:
            schedule_id_node = document.createElement(SCHEDULE_ID_NODE)
            schedule.appendChild(schedule_id_node)
            schedule_id_node.appendChild(document.createTextNode(self.schedule_id_))
        # user param
        if self.user_param_ != None:
            user_param_node = document.createElement(SCHEDULE_USER_PARAM_NODE)
            schedule.appendChild(user_param_node)
            user_param_node.appendChild(document.createTextNode(self.user_param_))
        # force add
        if self.force_add_:
            force_add_node = document.createElement(SCHEDULE_FORCE_ADD_NODE)
            schedule.appendChild(force_add_node)
            force_add_node.appendChild(document.createTextNode(XMLNODE_VALUE_TRUE))
        # by epg
        if self.by_epg_ != None:
            by_epg_node = self.by_epg_.create_node(document)
            schedule.appendChild(by_epg_node)
        # manual
        if self.manual_ != None:
            manual_node = self.manual_.create_node(document)
            schedule.appendChild(manual_node)        
        return document.toxml(encoding=XMLDOC_CODEPAGE)
    
    def init_from_xml(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)    
    
    def from_xml_(self, xml_string):
        schedule = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.schedule_id_ = str(schedule.getElementsByTagName(SCHEDULE_ID_NODE)[0].firstChild.data)
        except:
            return False
        try:
            self.user_param_ = str(schedule.getElementsByTagName(SCHEDULE_USER_PARAM_NODE)[0].firstChild.data)
        except:
            self.user_param_ = ""
        try:
            self.is_force_add_ = string_to_bool(schedule.getElementsByTagName(SCHEDULE_FORCE_ADD_NODE)[0].firstChild.data)
        except:
            self.is_force_add_ = False        
        try:
            self.by_epg_ = ByEpgSchedule()
            self.by_epg_.init_from_xml(schedule.getElementsByTagName(SCHEDULE_BY_EPG_ROOT_NODE)[0].toxml())
        except:
            self.by_epg_ = None
        try:
            self.manual_ = ManualSchedule()
            self.manual_.init_from_xml(schedule.getElementsByTagName(SCHEDULE_MANUAL_ROOT_NODE)[0].toxml())
        except:
            self.manual_ = None
        return True       

class ByEpgSchedule:

    def __init__(self, channel_id = None, program_id = None, is_repeat = False):
        self.channel_id_ = channel_id
        self.program_id_ = program_id
        self.is_repeat_ = is_repeat
    
    @property
    def channel_id(self):
        return self.channel_id_
    
    @property
    def title(self):
        return self.program_.name
    
    @property
    def start_time(self):
        return self.program_.start_time
    
    @property
    def duration(self):
        return self.program_.duration
        
    @property
    def program_id(self):
        return self.program_id_
        
    @property
    def is_repeat(self):
        return self.is_repeat_
        
    @property
    def is_new_only(self):
        return self.is_new_only_
        
    @property
    def is_record_series_anytime(self):
        return self.is_record_series_anytime_
    
    @property    
    def recordings_to_keep(self):
        return self.recordings_to_keep_
       
    def create_node(self, document):
        by_epg = document.createElement(SCHEDULE_BY_EPG_ROOT_NODE)
        # channel_id
        channel_id_node = document.createElement(SCHEDULE_CHANNEL_ID_NODE)
        by_epg.appendChild(channel_id_node)
        channel_id_node.appendChild(document.createTextNode(self.channel_id_))
        # program_id
        program_id_node = document.createElement(SCHEDULE_PROGRAM_ID_NODE)
        by_epg.appendChild(program_id_node)
        program_id_node.appendChild(document.createTextNode(self.program_id_))
        # is_repeat
        if self.is_repeat_:
            is_repeat_node = document.createElement(SCHEDULE_REPEATE_NODE)
            by_epg.appendChild(is_repeat_node)
            is_repeat_node.appendChild(document.createTextNode(XMLNODE_VALUE_TRUE))
        return by_epg
    
    def init_from_xml(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)    
    
    def from_xml_(self, xml_string):
        schedule = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.channel_id_ = str(schedule.getElementsByTagName(SCHEDULE_CHANNEL_ID_NODE)[0].firstChild.data)
            self.program_id_ = str(schedule.getElementsByTagName(SCHEDULE_PROGRAM_ID_NODE)[0].firstChild.data)
            self.program_ = Program(schedule.getElementsByTagName(EPG_PROGRAM)[0].toxml())
        except:
            return False
        try:
            self.is_repeat_ = string_to_bool(schedule.getElementsByTagName(SCHEDULE_REPEATE_NODE)[0].firstChild.data)
        except:
            self.is_repeat_ = False
        try:
            self.is_new_only_ = string_to_bool(schedule.getElementsByTagName(SCHEDULE_NEW_ONLY_NODE)[0].firstChild.data)
        except:
            self.is_new_only_ = False
        try:
            self.is_record_series_anytime_ = string_to_bool(schedule.getElementsByTagName(SCHEDULE_SERIES_ANYTIME_NODE)[0].firstChild.data)
        except:
            self.is_record_series_anytime_ = False
        try:
            self.recordings_to_keep_ = int(schedule.getElementsByTagName(SCHEDULE_REC_TO_KEEP_NODE)[0].firstChild.data)
        except:
            self.recordings_to_keep_ = 0

class ManualSchedule:
    
    DAY_MASK_ONCE = 0
    DAY_MASK_SUN = 1
    DAY_MASK_MON = 2
    DAY_MASK_TUE = 4
    DAY_MASK_WED = 8
    DAY_MASK_THU = 16
    DAY_MASK_FRI = 32
    DAY_MASK_SAT = 64
    DAY_MASK_DAILY = 255

    def __init__(self, channel_id = None, title = None, start_time = None, duration = None, day_mask = None):
        self.channel_id_ = channel_id
        self.title_ = title
        self.start_time_ = start_time
        self.duration_ = duration
        self.day_mask_ = day_mask
    
    @property
    def channel_id(self):
        return self.channel_id_
        
    @property
    def title(self):
        return self.title_
    
    @property
    def start_time(self):
        return self.start_time_
    
    @property
    def duration(self):
        return self.duration_
    
    @property
    def day_mask(self):
        return self.day_mask_
        
    @property
    def recordings_to_keep(self):
        return self.recordings_to_keep_
        
    def create_node(self, document):
        manual = document.createElement(SCHEDULE_MANUAL_ROOT_NODE)
        # channel_id
        channel_id_node = document.createElement(SCHEDULE_CHANNEL_ID_NODE)
        manual.appendChild(channel_id_node)
        channel_id_node.appendChild(document.createTextNode(self.channel_id_))
        # title
        title_node = document.createElement(SCHEDULE_TITLE_NODE)
        manual.appendChild(title_node)
        title_node.appendChild(document.createTextNode(self.title_.decode(XMLDOC_CODEPAGE)))
        # start time
        start_time_node = document.createElement(SCHEDULE_START_TIME_NODE)
        manual.appendChild(start_time_node)
        start_time_node.appendChild(document.createTextNode(str(self.start_time_)))
        # duration
        duration_node = document.createElement(SCHEDULE_DURATION_TIME_NODE)
        manual.appendChild(duration_node)
        duration_node.appendChild(document.createTextNode(str(self.duration_)))
        # day_mask
        mask_node = document.createElement(SCHEDULE_DAY_MASK_NODE)
        manual.appendChild(mask_node)
        mask_node.appendChild(document.createTextNode(str(self.day_mask_)))
        return manual
        
    def init_from_xml(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)    
    
    def from_xml_(self, xml_string):
        schedule = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.channel_id_ = str(schedule.getElementsByTagName(SCHEDULE_CHANNEL_ID_NODE)[0].firstChild.data)
            self.start_time_ = long(schedule.getElementsByTagName(SCHEDULE_START_TIME_NODE)[0].firstChild.data)
            self.duration_ = int(schedule.getElementsByTagName(SCHEDULE_DURATION_TIME_NODE)[0].firstChild.data)
        except:
            return False
        try:
            self.title_ = schedule.getElementsByTagName(SCHEDULE_TITLE_NODE)[0].firstChild.data
        except:
            self.title_ = ""
        try:
            self.day_mask_ = int(schedule.getElementsByTagName(SCHEDULE_DAY_MASK_NODE)[0].firstChild.data)
        except:
            self.day_mask_ = self.DAY_MASK_ONCE
        try:
            self.recordings_to_keep_ = int(schedule.getElementsByTagName(SCHEDULE_REC_TO_KEEP_NODE)[0].firstChild.data)
        except:
            self.recordings_to_keep_ = 0
        return True
                   
class Schedules(list):

    def __init__(self, xml_string):
        if self.from_xml_(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
            
    def from_xml_(self, xml_string):
        document = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        for schedule_node in document.getElementsByTagName(SCHEDULE_ROOT_NODE):
            try:
                schedule = Schedule()
                schedule.init_from_xml(schedule_node.toxml())
            except:
                pass
            else:
                self.append(schedule)
        return True