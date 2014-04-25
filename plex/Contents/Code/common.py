import time
import datetime
from constants import *

class DVBLinkStatus:
    STATUS_OK = 0
    STATUS_ERROR = 1000
    STATUS_INVALID_DATA = 1001
    STATUS_INVALID_PARAM = 1002
    STATUS_NOT_IMPLEMENTED = 1003
    STATUS_MC_NOT_RUNNING = 1005
    STATUS_NO_DEFAULT_RECORDER = 1006
    STATUS_MCE_CONNECTION_ERROR = 1008
    STATUS_CONNECTION_ERROR = 2000
    STATUS_UNAUTHORISED = 2001
                
class DVBLinkError(Exception):
    def __init__(self, value):
        self.value_ = value
        
    @property
    def value(self):
        return self.value_

def string_to_bool(string):
    if string and string.lower() == "true":
        return True
    return False

def bool_to_string(bool):
    if bool:
        return "True"
    return "False"

def datetime_to_ctime(date_time):
    return long(time.mktime(date_time.timetuple()))

def ctime_to_datetime(seconds):
    return datetime.datetime.fromtimestamp(seconds)

def get_time(seconds):
    date_time = ctime_to_datetime(seconds)
    return date_time.strftime('%H:%M')

def get_date(seconds):
    date_time = ctime_to_datetime(seconds)
    return date_time.strftime('%a, %d %b')
	
def is_time_today(seconds):
	date = ctime_to_datetime(seconds).date()
	if date == datetime.datetime.today().date():
		return True
	return False
	
def is_current_program(program):
	time_now = datetime_to_ctime(datetime.datetime.now())
	end_time = program.start_time + program.duration
	return (time_now >= program.start_time and time_now < end_time)

def get_channel_info_by_number(channel): 
    channel_info = ""
    if channel.channel_name:
        str_channel_number = get_channel_number_string(channel)
        if str_channel_number:
            channel_info += str_channel_number + "  "
        channel_info += channel.channel_name
    return channel_info
	
def get_channel_info_by_name(channel):
	channel_info = ""
	if channel.channel_name:
		channel_info += channel.channel_name
		str_channel_number = get_channel_number_string(channel)
		if str_channel_number:
			channel_info += "  (" + str_channel_number + ")"
	return channel_info

def get_channel_number_string(channel):
    if channel.channel_number > -1:
        str_channel_number = str(channel.channel_number)
        if channel.channel_subnumber > 0:
            str_channel_number += "." + str(channel.channel_subnumber)
        return str_channel_number
    return ""
	
def search_recording(recordings, program_id, channel_id):
	for recording in recordings:
		try:
			if recording.channel_id == channel_id and recording.program.program_id == program_id:
				return recording
		except:
			pass
	return None

def search_channel(channels, channel_id):
    channel_list = [channel for channel in channels if channel.channel_id == channel_id]
    return channel_list[0] if len(channel_list) else None