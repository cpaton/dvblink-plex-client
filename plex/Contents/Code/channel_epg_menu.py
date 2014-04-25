import helper
import common
import datetime
from actions_menu import actions_menu
from data_provider import data_provider
from localization import *
from control_recorder import ControlRecorder

class ChannelEPGMenu(object):
	
	# private fields
	channel_id_ = None
	channel_name_ = None
	recording_list_ = []
	control_recorder_ = None
	
	def __init__(self):
		self.control_recorder_ = ControlRecorder()
		
	def create(self, channel_name, channel_id):
		try:
			self.channel_name_ = channel_name
			self.channel_id_ = channel_id
			return self.create_channel_epg_list_()
		except common.DVBLinkError, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=helper.get_status_string_id(error))
		except Exception, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=str(error))
	
	def create_program_actions(self, title, program_id, is_series, replace_parent=False):
		return actions_menu.create(title, program_id, self.channel_id_, self.channel_name_, is_series, R(helper.ART_TV_GUIDE), replace_parent)
			
	def	create_channel_epg_list_(self):
		oc = ObjectContainer(
			no_history = True,
			no_cache = True,
			title1 = IDS_GUIDE_MENU_ITEM,
			title2 = self.channel_name_,
			art = R(helper.ART_TV_GUIDE))
			
		time_now = common.datetime_to_ctime(datetime.datetime.now())
		programs_dict = data_provider.get_channel_epg(self.channel_id_)
		self.recording_list_ = data_provider.get_recordings()
		if None != programs_dict and programs_dict.has_key(self.channel_id_):
			channel_programs = programs_dict[self.channel_id_]
			for program in channel_programs:
				if time_now < program.start_time + program.duration:
					program_object = self.create_program_item_(program)
					oc.add(program_object)
		return oc
		
	def create_program_item_(self, program):
		recording = common.search_recording(self.recording_list_, program.program_id, self.channel_id_)
		is_record = recording.program.is_record if recording else False
		is_series_record = recording.program.is_repeat_record if recording else False
		is_conflicting = recording.is_conflicting if recording else False
		title = helper.create_program_title(program, is_record, is_series_record, is_conflicting)
		return TVShowObject(
			key = Callback(
				self.create_program_actions, 
				title = program.name,
				program_id = program.program_id,
				is_series = program.is_series),
			rating_key = program.program_id,
			title = title,
			summary = helper.create_program_summary(program),
			source_title = self.channel_name_,
			rating = float(helper.calculate_rating(program.stars_number, program.stars_max_number)),
			originally_available_at = Datetime.FromTimestamp(program.start_time).date(),
			duration = program.duration * 1000,
			genres = program.keywords.split('/') if program.keywords else [],
			thumb = Resource.ContentsOfURLWithFallback(program.image))
		
channel_epg_menu = ChannelEPGMenu()