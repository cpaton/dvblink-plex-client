import helper
import common
import datetime
from data_provider import data_provider
from control_recorder import ControlRecorder
from localization import *

class ActionsMenu(object):
	
	# private fields
	recording_list_ = []
	recording_only_ = False
	
	def __init__(self):
		self.control_recorder_ = ControlRecorder()
	
	def create(self, title, program_id, channel_id, channel_name, is_series, art, replace_parent, recording_only=False):
		try:
			self.recording_only_ = recording_only
			self.recording_list_ = self.get_recordings_()
			return self.create_actions_menu(title, program_id, channel_id, channel_name, is_series, art, replace_parent)
		except common.DVBLinkError, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=helper.get_status_string_id(error))
		except Exception, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=str(error))
	
	def create_actions_menu(self, title, program_id, channel_id, channel_name, is_series, art, replace_parent):
		recording = common.search_recording(self.recording_list_, program_id, channel_id)
		is_record = recording.program.is_record if recording else False
		is_series_record = recording.program.is_repeat_record if recording else False
		
		oc = ObjectContainer(
			no_history = True,
			no_cache = True,
			replace_parent = replace_parent,
			title1 = channel_name,
			title2 = title,
			art = art)
		
		if self.recording_only_ and not recording:
			return oc
		
		if is_record:
			oc.add(DirectoryObject(
				key = Callback(
					self.cancel_recording,
					title = title,
					program_id = program_id,
					channel_id = channel_id,
					channel_name = channel_name,
					is_series = is_series,
					recording_id = recording.recording_id),
				title = IDS_CANCEL_RECORDING,
				thumb = R(helper.ICON_CANCEL_RECORDING)))
		else:
			oc.add(DirectoryObject(
				key = Callback(
					self.add_recording,
					title = title,
					program_id = program_id,
					channel_id = channel_id,
					channel_name = channel_name,
					is_series = is_series),
				title = IDS_ADD_RECORDING,
				thumb = R(helper.ICON_ADD_RECORDING)))
				
		if is_series or is_series_record:
			if is_series_record:
				oc.add(DirectoryObject(
					key = Callback(
						self.cancel_series,
						title = title,
						program_id = program_id,
						channel_id = channel_id,
						channel_name = channel_name,
						is_series = is_series,
						schedule_id = recording.schedule_id),
					title = IDS_CANCEL_RECORD_SERIES,
					thumb = R(helper.ICON_CANCEL_SERIES)))
			else:
				oc.add(DirectoryObject(
					key = Callback(
						self.add_series, 
						title = title,
						program_id = program_id,
						channel_id = channel_id,
						channel_name = channel_name,
						is_series = is_series),
					title = IDS_RECORD_SERIES,
					thumb = R(helper.ICON_ADD_SERIES)))			
		
		return oc
	
	def add_recording(self, title, program_id, channel_id, channel_name, is_series):
		if self.control_recorder_.add_recording(channel_id, program_id):
			self.recording_list_ = self.get_recordings_()
			return self.create_actions_menu(title, program_id, channel_id, channel_name, is_series, True)
		else:
			return MessageContainer(
				header = IDS_CAPTION_ERROR,
				message = IDS_ADD_RECORDING_ERROR_MSG)
		
	def cancel_recording(self, title, program_id, channel_id, channel_name, is_series, recording_id):
		if self.control_recorder_.cancel_recording(recording_id):
			self.recording_list_ = self.get_recordings_()
			return self.create_actions_menu(title, program_id, channel_id, channel_name, is_series, True)
		else:
			return MessageContainer(
				header = IDS_CAPTION_ERROR,
				message = IDS_CANCEL_RECORDING_ERROR_MSG)
		
	def add_series(self, title, program_id, channel_id, channel_name, is_series):
		if self.control_recorder_.add_series(channel_id, program_id):
			self.recording_list_ = self.get_recordings_()
			return self.create_actions_menu(title, program_id, channel_id, channel_name, is_series, True)
		else:
			return MessageContainer(
				header = IDS_CAPTION_ERROR,
				message = IDS_ADD_SCHEDULE_ERROR_MSG)
	
	def cancel_series(self, title, program_id, channel_id, channel_name, is_series, schedule_id):
		if self.control_recorder_.cancel_series(schedule_id):
			self.recording_list_ = self.get_recordings_()
			return self.create_actions_menu(title, program_id, channel_id, channel_name, is_series, True)
		else:
			return MessageContainer(
				header = IDS_CAPTION_ERROR,
				message = IDS_CANCEL_SCHEDULE_ERROR_MSG)
	
	def get_recordings_(self):
		recordings = data_provider.get_recordings()
		if self.recording_only_:
			return [recording for recording in recordings if recording.program and recording.program.is_record]
		return recordings
	
actions_menu = ActionsMenu()