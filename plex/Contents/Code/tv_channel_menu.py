import helper
import common
import datetime
from data_provider import data_provider
from localization import *

class TVChannelMenu(object):
	
	PROGRAM_COUNT_ = 3
	
	# private fields
	channel_list_ = []
	stream_info_dict_ = {}
	current_program_dict_ = {}
	sort_mode_ = helper.SortMode.BY_NUMBER
	
	def create(self):
		try:
			if not self.channel_list_:
				self.sort_mode_ = self.get_sort_mode_()
				self.get_channels_()
			if not self.channel_list_ or not self.stream_info_dict_:
				return MessageContainer(
					header=IDS_CAPTION_WARNING,
					message=IDS_CHANNELS_NOT_AVALIABLE)
			self.current_program_dict_ = self.get_preview_programs_()
			return self.create_channel_list_()
		except common.DVBLinkError, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=helper.get_status_string_id(error))
		except Exception, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=str(error))
	
	def reset(self):
		self.channel_list_ = []
		self.stream_info_dict_ = {}
		self.current_program_dict_ = {}
	
	def create_tv_channel_object(self, channel_name, channel_title, channel_id, stream_url, include_container=False):
		channel_object = VideoClipObject(
			key = Callback(
				self.create_tv_channel_object,
				channel_name = channel_name,
				channel_title = channel_title, 
				channel_id = channel_id, 
				stream_url = stream_url, 
				include_container = True),
			rating_key = channel_id,
			title = channel_title,
			source_title = channel_name,
			summary = self.create_programs_summary_(channel_id),
			thumb = R(helper.ICON_TV_CHANNEL),
			items = [
				MediaObject(
					parts = [
						PartObject(key=Callback(self.play_tv_channel, url=stream_url))
					]
				)
			]
		)
		
		if include_container:
			return ObjectContainer(objects=[channel_object])
		else:
			return channel_object
	
	def play_tv_channel(self, url):
		return Redirect(url)
		
	def get_sort_mode_(self):
		return (helper.SortMode.BY_NUMBER if str(L(Prefs[helper.CHANNEL_SORT_MODE_KEY])) == str(IDS_BY_NUMBER) else helper.SortMode.BY_NAME)
		
	def create_channel_list_(self):
		oc = ObjectContainer(
			no_history = True,
			no_cache = True,
			title2 = IDS_CHANNEL_MENU_ITEM,
			art = R(helper.ART_TV_CHANNELS))
		for channel in self.channel_list_:
			channel_object = self.create_tv_channel_object(
				channel.channel_name,
				common.get_channel_info_by_number(channel) if self.sort_mode_ == helper.SortMode.BY_NUMBER else common.get_channel_info_by_name(channel),
				channel.channel_id,
				self.stream_info_dict_.get(channel.dvblink_channel_id, None))
			oc.add(channel_object)
		return oc
	
	def create_programs_summary_(self, channel_id):
		summary = ""
		current_program_list = self.current_program_dict_.get(channel_id, None)
		program_1 = current_program_list[0]	if None != current_program_list and len(current_program_list) > 0 else None
		program_2 = current_program_list[1]	if None != current_program_list and len(current_program_list) > 1 else None
		program_3 = current_program_list[2] if None != current_program_list and len(current_program_list) > 2 else None
		if program_1:
			summary += self.create_program_summary(program_1)
		else:
			if program_2 or program_3:
				summary += "%s\n\n" % IDS_DATA_NOT_AVAILABLE
		if program_2:
			summary += self.create_program_summary(program_2)
		if program_3:
			summary += self.create_program_summary(program_3)
		return summary
	
	def create_program_summary(self, program):
		return "%s\n\n" % helper.create_program_title(program, program.is_record, program.is_repeat_record, False)
	
	def get_channels_(self):
		self.channel_list_ = data_provider.get_tv_channels()
		self.stream_info_dict_ = data_provider.get_stream_info()
		if self.channel_list_:
			if helper.SortMode.BY_NAME == self.sort_mode_:
				self.channel_list_.sort(key=lambda channel: channel.channel_name)
			else:
				self.channel_list_.sort(key=lambda channel: (channel.channel_number, channel.channel_subnumber)) 
	
	def get_preview_programs_(self):
		preview_programs_dict = {}
		time_now = common.datetime_to_ctime(datetime.datetime.now())
		current_dict = data_provider.get_actual_programs(self.PROGRAM_COUNT_)
		for channel_id, program_list in current_dict.items():
			if None != program_list and len(program_list):
				start_time = program_list[0].start_time
				end_time = start_time + program_list[0].duration
				if not (time_now >= start_time and time_now < end_time):
					program_list.insert(0, None)
				for i, v in enumerate(program_list[:-1]):
					if program_list[i] and program_list[i + 1].start_time != (program_list[i].start_time + program_list[i].duration):
						program_list.insert(i + 1, None)
				program_list += [None,] * (self.PROGRAM_COUNT_ - 1)
				program_list = program_list[:self.PROGRAM_COUNT_]
			preview_programs_dict[channel_id] = program_list
		return preview_programs_dict
		
tv_channel_menu = TVChannelMenu()