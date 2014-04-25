import helper
import common
from actions_menu import actions_menu
from data_provider import data_provider
from control_recorder import ControlRecorder
from localization import *
from recordings import *

class RecordingsMenu(object):
	
	# private fields
	channel_list_ = []
	recording_list_ = []
	
	def __init__(self):
		self.control_recorder_ = ControlRecorder()
		
	def create(self):
		try:
			if not self.channel_list_:
				self.channel_list_ = data_provider.get_channels()
			return self.create_recordings_list_()
		except common.DVBLinkError, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=helper.get_status_string_id(error))
		except Exception, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=str(error))

	def create_recording_actions(self, title, program_id, channel_id, channel_name, is_series, replace_parent=False):
		return actions_menu.create(
			title, 
			program_id, 
			channel_id, 
			channel_name, 
			is_series, 
			R(helper.ART_SCHEDULED_RECORDINGS), 
			replace_parent,
			True)
	
	def create_recordings_list_(self):
		oc = ObjectContainer(
			no_history = True,
			no_cache = True,
			title2 = IDS_SCHEDULED_RECORDINGS_MENU_ITEM,
			art = R(helper.ART_SCHEDULED_RECORDINGS))
			
		self.recording_list_ = self.get_recordings_()
		if self.recording_list_:
			self.recording_list_.sort(key=lambda recording: recording.program.start_time)
			for recording in self.recording_list_:
				oc.add(self.create_recording_item_(recording))
		return oc
		
	def create_recording_item_(self, recording):
		program = recording.program
		channel = common.search_channel(self.channel_list_, recording.channel_id)
		title = helper.create_recording_title(program, program.is_record, program.is_repeat_record, recording.is_conflicting)
		return TVShowObject(
			key = Callback(
				self.create_recording_actions, 
				title = program.name,
				program_id = program.program_id,
				channel_id = recording.channel_id,
				channel_name = channel.channel_name if channel else IDS_UNKNOWN,
				is_series = program.is_series),
			rating_key = program.program_id,
			title = title,
			summary = helper.create_program_summary(program),
			source_title = channel.channel_name if channel else IDS_UNKNOWN,
			rating = float(helper.calculate_rating(program.stars_number, program.stars_max_number)),
			originally_available_at = Datetime.FromTimestamp(program.start_time).date(),
			duration = program.duration * 1000,
			genres = program.keywords.split('/') if program.keywords else [],
			thumb = Resource.ContentsOfURLWithFallback(program.image))
	
	def get_recordings_(self):
		return [recording for recording in data_provider.get_recordings() \
			if recording.program and recording.program.is_record]
	
	def search_recording_(self, recording_id):
		recording_list = [recording for recording in self.recording_list_ if recording.recording_id == recording_id]
		return recording_list[0] if len(recording_list) else None
	
recordings_menu = RecordingsMenu()