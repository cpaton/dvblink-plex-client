import helper
import common
from channel_epg_menu import channel_epg_menu
from data_provider import data_provider
from localization import *

class GuideMenu(object):
	
	# private fields
	channel_list_ = []
	sort_mode_ = helper.SortMode.BY_NUMBER
	
	def create(self):
		try:
			if not self.channel_list_:
				self.sort_mode_ = self.get_sort_mode_()
				self.get_channels_()
			if not self.channel_list_:
				return MessageContainer(
					header=IDS_CAPTION_WARNING,
					message=IDS_CHANNELS_NOT_AVALIABLE)
			return self.create_guide_list_()
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

	def create_epg_menu(self, channel_name, channel_id):
		return channel_epg_menu.create(channel_name, channel_id)
		
	def play_channel(self, url):
		return Redirect(url)
		
	def get_sort_mode_(self):
		return (helper.SortMode.BY_NUMBER if str(L(Prefs[helper.CHANNEL_SORT_MODE_KEY])) == str(IDS_BY_NUMBER) else helper.SortMode.BY_NAME)
		
	def create_guide_list_(self):
		oc = ObjectContainer(
			no_history = True,
			no_cache = True,
			title2 = IDS_GUIDE_MENU_ITEM,
			art = R(helper.ART_TV_GUIDE))
		for channel in self.channel_list_:
			oc.add(self.create_guide_item_(channel))
		return oc
	
	def create_guide_item_(self, channel):
		channel_title = common.get_channel_info_by_number(channel) if self.sort_mode_ == helper.SortMode.BY_NUMBER else common.get_channel_info_by_name(channel)
		channel_object = DirectoryObject(
			key = Callback(
				self.create_epg_menu,
				channel_name = channel.channel_name,
				channel_id = channel.channel_id),
			title = channel_title,
			thumb = R(helper.ICON_TV_GUIDE_CHANNEL))
		return channel_object
	
	def get_channels_(self):
		self.channel_list_ = data_provider.get_channels()
		if self.channel_list_:
			if helper.SortMode.BY_NAME == self.sort_mode_:
				self.channel_list_.sort(key=lambda channel: channel.channel_name)
			else:
				self.channel_list_.sort(key=lambda channel: (channel.channel_number, channel.channel_subnumber)) 
				
guide_menu = GuideMenu()