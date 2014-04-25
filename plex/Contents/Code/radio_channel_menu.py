import helper
import common
import datetime
from data_provider import data_provider
from localization import *

class RadioChannelMenu(object):
	
	# private fields
	channel_list_ = []
	stream_info_dict_ = {}
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
	
	def create_radio_channel_object(self, channel_name, channel_title, channel_id, stream_url, include_container=False):
		channel_object = TrackObject(
			key = Callback(
				self.create_radio_channel_object,
				channel_name = channel_name,
				channel_title = channel_title, 
				channel_id = channel_id, 
				stream_url = stream_url, 
				include_container = True),
			rating_key = channel_id,
			title = channel_title,
			source_title = channel_name,
			thumb = R(helper.ICON_RADIO_CHANNEL),
			items = [
				MediaObject(
					parts = [
						PartObject(key=Callback(self.play_radio_channel, url=stream_url))
					]
				)
			]
		)
		
		if include_container:
			return ObjectContainer(objects=[channel_object])
		else:
			return channel_object
	
	def play_radio_channel(self, url):
		return Redirect(url)
		
	def get_sort_mode_(self):
		return (helper.SortMode.BY_NUMBER if str(L(Prefs[helper.CHANNEL_SORT_MODE_KEY])) == str(IDS_BY_NUMBER) else helper.SortMode.BY_NAME)
		
	def create_channel_list_(self):
		oc = ObjectContainer(
			no_history = True,
			no_cache = True,
			title2 = IDS_CHANNEL_MENU_ITEM,
			art = R(helper.ART_RADIO_CHANNELS))
		for channel in self.channel_list_:
			channel_object = self.create_radio_channel_object(
				channel.channel_name,
				common.get_channel_info_by_number(channel) if self.sort_mode_ == helper.SortMode.BY_NUMBER else common.get_channel_info_by_name(channel),
				channel.channel_id,
				self.stream_info_dict_.get(channel.dvblink_channel_id, None))
			oc.add(channel_object)
		return oc
	
	def get_channels_(self):
		self.channel_list_ = data_provider.get_radio_channels()
		self.stream_info_dict_ = data_provider.get_stream_info()
		if self.channel_list_:
			if helper.SortMode.BY_NAME == self.sort_mode_:
				self.channel_list_.sort(key=lambda channel: channel.channel_name)
			else:
				self.channel_list_.sort(key=lambda channel: (channel.channel_number, channel.channel_subnumber)) 
		
radio_channel_menu = RadioChannelMenu()