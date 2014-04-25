import helper
from tv_channel_menu import tv_channel_menu
from radio_channel_menu import radio_channel_menu
from channels import *
from guide_menu import guide_menu
from recorded_tv_menu import recorded_tv_menu
from channel_epg_menu import channel_epg_menu
from recordings_menu import recordings_menu
from search_menu import search_menu
from actions_menu import actions_menu
from localization import *
from data_provider import data_provider

def Start():
	Plugin.AddPrefixHandler("/video/dvblink", MainMenu, IDS_PLUGIN_TITLE, helper.ICON_PLUGIN, helper.ART_PLUGIN)
	Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
	
	ObjectContainer.title1 = IDS_PLUGIN_TITLE
	ObjectContainer.view_group = "InfoList"
	ObjectContainer.art = R(helper.ART_PLUGIN)
	
	init_plugin()	

def MainMenu():
	oc = ObjectContainer()
	
	oc.add(DirectoryObject(
        key = Callback(create_channel_menu), 
		title = IDS_CHANNEL_MENU_ITEM,
		thumb = R(helper.ICON_TV_CHANNELS),
		art = R(helper.ART_TV_CHANNELS)))
		
	oc.add(DirectoryObject(
        key = Callback(create_radio_menu), 
		title = IDS_RADIO_MENU_ITEM,
		thumb = R(helper.ICON_RADIO_CHANNELS),
		art = R(helper.ART_RADIO_CHANNELS)))
	
	oc.add(DirectoryObject(
		key = Callback(create_guide_menu),
		title = IDS_GUIDE_MENU_ITEM,
		thumb = R(helper.ICON_TV_GUIDE),
		art = R(helper.ART_TV_GUIDE)))
		
	oc.add(DirectoryObject(
		key = Callback(create_recorded_tv_menu),
		title = IDS_RECORDED_TV_MENU_ITEM,
		thumb = R(helper.ICON_RECORDED_TV),
		art = R(helper.ART_RECORDED_TV)))
	
	oc.add(DirectoryObject(
		key = Callback(create_scheduled_recordings_menu),
		title = IDS_SCHEDULED_RECORDINGS_MENU_ITEM,
		thumb = R(helper.ICON_SCHEDULED_RECORDINGS),
		art = R(helper.ART_SCHEDULED_RECORDINGS)))
	
	oc.add(DirectoryObject(
		key = Callback(create_search_menu),
		title = IDS_SEARCH_MENU_ITEM,
		thumb = R(helper.ICON_SEARCH),
		art = R(helper.ART_SEARCH)))	
	
	oc.add(PrefsObject(
		title = IDS_SETTINGS_MENU_ITEM,
		thumb = R(helper.ICON_SETTINGS),
		art = R(helper.ART_SETTINGS)))
	
	return oc

def ValidatePrefs():
	if not validate_port():
		return MessageContainer(
			header=IDS_CAPTION_ERROR,
			message=IDS_PORT_VALIDATOR_MSG)
	init_plugin()
			
def init_plugin():
	# generate plugin id if not exists
	if not Data.Exists(helper.PLUGIN_UUID_KEY):
		Data.Save(helper.PLUGIN_UUID_KEY, String.UUID())
	plugin_id = Data.Load(helper.PLUGIN_UUID_KEY)

	data_provider.init(plugin_id,
		Prefs[helper.SERVER_ADDRESS_KEY], 
		int(Prefs[helper.SERVER_PORT_KEY]) if validate_port() else helper.SERVER_PORT_DEFAULT_VALUE,
		Prefs[helper.USER_NAME_KEY],
		Prefs[helper.PASSWORD_KEY],
		False, 
		helper.get_epg_of_days(str(L(Prefs[helper.EPG_OF_DAYS_ID_KEY]))))
	tv_channel_menu.reset()
	radio_channel_menu.reset()
	
def validate_port():
	try:
		server_port = Prefs[helper.SERVER_PORT_KEY]
		if int(server_port) >= helper.MIN_SERVER_PORT and int(server_port) <= helper.MAX_SERVER_PORT:
			return True
	except:
		pass
	return False
				
# Main menu
def create_channel_menu():
	return tv_channel_menu.create()

def create_radio_menu():
	return radio_channel_menu.create()

def create_guide_menu():
	return guide_menu.create()

def create_recorded_tv_menu():
	return recorded_tv_menu.create()
	
def create_scheduled_recordings_menu():
	return recordings_menu.create()

def create_search_menu():
	return search_menu.create()
	
# class TVChannelMenu	
def play_tv_channel(url):
	return tv_channel_menu.play_tv_channel(url)

def create_tv_channel_object(channel_name, channel_title, channel_id, stream_url, include_container=False):
	return tv_channel_menu.create_tv_channel_object(channel_name, channel_title, channel_id, stream_url, include_container)

# class RadioChannelMenu	
def play_radio_channel(url):
	return radio_channel_menu.play_radio_channel(url)

def create_radio_channel_object(channel_name, channel_title, channel_id, stream_url, include_container=False):
	return radio_channel_menu.create_radio_channel_object(channel_name, channel_title, channel_id, stream_url, include_container)
		
# class GuideMenu	
def create_epg_menu(channel_name, channel_id):
	return guide_menu.create_epg_menu(channel_name, channel_id)
		
# class RecordedTVMenu
def create_recorded_tv_list(title, object_id):
	return recorded_tv_menu.create_recorded_tv_list(title, object_id)

def create_recorded_tv_item(url, object_id, title, source_title, summary, rating, start_time, duration, year, writers, directors, producers, guests, genres, thumbnail, include_container=False):
	return recorded_tv_menu.create_recorded_tv_item(url, object_id, title, source_title, summary, rating, start_time, duration, year, writers, directors, producers, guests, genres, thumbnail, include_container)

def play_recording(url):
	return recorded_tv_menu.play_recording(url)
	
# class ChannelEPGMenu
def create_program_actions(title, program_id, is_series, replace_parent=False):
	return channel_epg_menu.create_program_actions(title, program_id, is_series, replace_parent)

# class RecordingsMenu
def create_recording_actions(title, program_id, channel_id, channel_name, is_series, replace_parent=False):
	return recordings_menu.create_recording_actions(title, program_id, channel_id, channel_name, is_series, replace_parent)
	
# class SearchMenu
def create_categories_menu():
	return search_menu.create_categories_menu()

def create_program_list_by_keyword(query):
	return search_menu.create_program_list_by_keyword(query)
	
def create_program_list_by_genre(title, genre_mask):
	return search_menu.create_program_list_by_genre(title, genre_mask)
	
def create_program_search_actions(title, program_id, channel_id, channel_name, is_series, replace_parent=False):
	return search_menu.create_program_search_actions(title, program_id, channel_id, channel_name, is_series, replace_parent)

# class ActionsMenu
def create_actions_menu(title, program_id, channel_id, channel_name, is_series, art, replace_parent):
	actions_menu.create_actions_menu(title, program_id, channel_id, channel_name, is_series, art, replace_parent)

def add_recording(title, program_id, channel_id, channel_name, is_series):
	return actions_menu.add_recording(title, program_id, channel_id, channel_name, is_series)
	
def cancel_recording(title, program_id, channel_id, channel_name, is_series, recording_id):
	return actions_menu.cancel_recording(title, program_id, channel_id, channel_name, is_series, recording_id)
	
def add_series(title, program_id, channel_id, channel_name, is_series):
	return actions_menu.add_series(title, program_id, channel_id, channel_name, is_series)
	
def cancel_series(title, program_id, channel_id, channel_name, is_series, schedule_id):
	return actions_menu.cancel_series(title, program_id, channel_id, channel_name, is_series, schedule_id)
	