import helper
import common
from constants import *
from localization import *
from schedules import *
from recordings import *
from data_provider import data_provider

class ControlRecorder(object):
    
	def __init__(self, callback_func = None):
		self.do_callback_func_ = callback_func
    
	def set_callback(self, callback_func):
		self.do_callback_func_ = callback_func
    
	def add_recording(self, channel_id, program_id):
		return self.add_recording_(channel_id, program_id)
    
	def cancel_recording(self, recording_id):
		try:
			data_provider.remove_recording(RecordingRemover(recording_id))
			if None != self.do_callback_func_:
				self.do_callback_func_()
			return True
		except common.DVBLinkError, error:
			helper.log_error('ControlRecorder.cancel_recording. ' + str(error))
		except Exception, error:
			helper.log_error('ControlRecorder.cancel_recording. ' + str(error))
		return False
    
	def add_series(self, channel_id, program_id):
		return self.add_recording_(channel_id, program_id, True)
    
	def cancel_series(self, schedule_id):
		try:
			data_provider.remove_schedule(ScheduleRemover(schedule_id))
			if None != self.do_callback_func_:
				self.do_callback_func_()
			return True
		except common.DVBLinkError, error:
			helper.log_error('ControlRecorder.cancel_series. ' + str(error))
		except Exception, error:
			helper.log_error('ControlRecorder.cancel_series. ' + str(error))
		return False
	
	def schedule_update(self, schedule_id, is_new_only, is_record_series_anytime, recordings_to_keep):
		try:
			data_provider.update_schedule(ScheduleUpdater(
				schedule_id = schedule_id,
				new_only = is_new_only, 
				record_series_anytime = is_record_series_anytime,
				recordings_to_keep = recordings_to_keep))
			if None != self.do_callback_func_:
				self.do_callback_func_()
			return True
		except common.DVBLinkError, error:
			helper.log_error('ControlRecorder.schedule_update. ' + str(error))
		except Exception, error:
			helper.log_error('ControlRecorder.schedule_update. ' + str(error))
		return False
        
	def add_recording_(self, channel_id, program_id, is_repeat=False):
		try:
			data_provider.add_schedule(Schedule(by_epg=ByEpgSchedule(channel_id, program_id, is_repeat)))
			if None != self.do_callback_func_:
				self.do_callback_func_()
			return True
		except common.DVBLinkError, error:
			helper.log_error('ControlRecorder.add_recording_. ' + str(error))
		except Exception, error:
			helper.log_error('ControlRecorder.add_recording_. ' + str(error))
		return False