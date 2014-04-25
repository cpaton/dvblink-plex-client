import helper
import common
import datetime
from actions_menu import actions_menu
from data_provider import data_provider
from control_recorder import ControlRecorder
from epg_searcher import GenreCategoryType
from localization import *

class SearchMenu(object):
	
	MIN_KEYWORDS_LEN_ = 3
	
	# private fields
	recording_list_ = []

	genre_category_values_ = {
		GenreCategoryType.ANY: str(IDS_GENRE_ANY),
		GenreCategoryType.NEWS: str(IDS_GENRE_NEWS),
		GenreCategoryType.KIDS: str(IDS_GENRE_KIDS),
		GenreCategoryType.MOVIE: str(IDS_GENRE_MOVIE),
		GenreCategoryType.SPORT: str(IDS_GENRE_SPORT),
		GenreCategoryType.DOCUMENTARY: str(IDS_GENRE_DOCUMENTARY),
		GenreCategoryType.ACTION: str(IDS_GENRE_ACTION),
		GenreCategoryType.COMEDY: str(IDS_GENRE_COMEDY),
		GenreCategoryType.DRAMA: str(IDS_GENRE_DRAMA),
		GenreCategoryType.EDU: str(IDS_GENRE_EDU),
		GenreCategoryType.HORROR: str(IDS_GENRE_HORROR),
		GenreCategoryType.MUSIC: str(IDS_GENRE_MUSIC),
		GenreCategoryType.REALITY: str(IDS_GENRE_REALITY),
		GenreCategoryType.ROMANCE: str(IDS_GENRE_ROMANCE),
		GenreCategoryType.SCIFI: str(IDS_GENRE_SCIFI),
		GenreCategoryType.SERIAL: str(IDS_GENRE_SERIAL),
		GenreCategoryType.SOAP: str(IDS_GENRE_SOAP),
		GenreCategoryType.SPECIAL: str(IDS_GENRE_SPECIAL),
		GenreCategoryType.THRILLER: str(IDS_GENRE_THRILLER),
		GenreCategoryType.ADULT: str(IDS_GENRE_ADULT)
	}
	
	def __init__(self):
		self.control_recorder_ = ControlRecorder()
		
	def create(self):
		return self.create_search_list_()
	
	def create_categories_menu(self):
		oc = ObjectContainer(
			no_history = True,
			no_cache = True,
			title1 = IDS_SEARCH_MENU_ITEM,
			title2 = IDS_CATEGORIES_MENU_ITEM,
			art = R(helper.ART_SEARCH))
			
		for key, value in sorted(self.genre_category_values_.items(), key=lambda v: (v[1], v[0])):
			if GenreCategoryType.ANY != key:
				oc.add(DirectoryObject(
					key = Callback(
						self.create_program_list_by_genre, 
						title = value,
						genre_mask = key), 
					title = value,
					thumb = R(helper.ICON_CATEGORIES)))
		return oc
	
	def create_program_list_by_keyword(self, query):
		try:
			if self.MIN_KEYWORDS_LEN_ > len(query):
				return MessageContainer(
					header=IDS_CAPTION_WARNING,
					message=IDS_ENTER_KEYWORD_WARNING)
			programs_dict = data_provider.search_epg_by_keywords(query)
			return self.create_program_list_(programs_dict, IDS_KEYWORD_MENU_ITEM, query)
		except common.DVBLinkError, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=helper.get_status_string_id(error))
		except Exception, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=str(error))
				
	def create_program_list_by_genre(self, title, genre_mask):
		try:
			programs_dict = data_provider.search_epg_by_genre(genre_mask)
			return self.create_program_list_(programs_dict, IDS_CATEGORIES_MENU_ITEM, title)
		except common.DVBLinkError, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=helper.get_status_string_id(error))
		except Exception, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=str(error))
	
	def create_program_search_actions(self, title, program_id, channel_id, channel_name, is_series, replace_parent=False):
		return actions_menu.create(title, program_id, channel_id, channel_name, is_series, R(helper.ART_SEARCH), replace_parent)
	
	def create_search_list_(self):
		oc = ObjectContainer(
			no_history = True,
			no_cache = True,
			title2 = IDS_SEARCH_MENU_ITEM,
			art = R(helper.ART_SEARCH))
	
		oc.add(InputDirectoryObject(
			key = Callback(self.create_program_list_by_keyword), 
			title = IDS_KEYWORD_MENU_ITEM,
			prompt = IDS_ENTER_KEYWORD_TITLE,
			thumb = R(helper.ICON_KEYWORD)))
		
		oc.add(DirectoryObject(
			key = Callback(self.create_categories_menu), 
			title = IDS_CATEGORIES_MENU_ITEM,
			thumb = R(helper.ICON_CATEGORIES)))
	
		return oc
	
	def create_program_list_(self, programs_dict, title_1, title_2):
		oc = ObjectContainer(
			no_history = True,
			no_cache = True,
			title1 = title_1,
			title2 = title_2,
			art = R(helper.ART_SEARCH))
		time_now = common.datetime_to_ctime(datetime.datetime.now())
		channels = data_provider.get_channels()
		#stream_info_dict = data_provider.get_stream_info()
		self.recording_list_ = data_provider.get_recordings(False)
		if len(programs_dict) and len(channels):
			program_list = self.get_programs_(programs_dict)
			for list_item in program_list:
				channel = common.search_channel(channels, list_item[0])
				if channel:
					program = list_item[1]
					if time_now < program.start_time + program.duration:
						program_object = self.create_program_item_(program, channel)
						oc.add(program_object)
		return oc
		
	def create_program_item_(self, program, channel):
		recording = common.search_recording(self.recording_list_, program.program_id, channel.channel_id)
		is_record = recording.program.is_record if recording else False
		is_series_record = recording.program.is_repeat_record if recording else False
		is_conflicting = recording.is_conflicting if recording else False
		title = helper.create_program_title(program, is_record, is_series_record, is_conflicting)
		return TVShowObject(
			key = Callback(
				self.create_program_search_actions, 
				title = program.name,
				program_id = program.program_id,
				channel_id = channel.channel_id,
				channel_name = channel.channel_name,
				is_series = program.is_series),
			rating_key = program.program_id,
			title = title,
			summary = helper.create_program_summary(program),
			source_title = channel.channel_name,
			rating = float(helper.calculate_rating(program.stars_number, program.stars_max_number)),
			originally_available_at = Datetime.FromTimestamp(program.start_time).date(),
			duration = program.duration * 1000,
			genres = program.keywords.split('/') if program.keywords else [],
			thumb = Resource.ContentsOfURLWithFallback(program.image))
	
	def get_programs_(self, programs_dict):
		program_list = []
		for key, value in programs_dict.items():
			for program in value:
				item = (key, program)
				program_list.append(item)
		if len(program_list):
			program_list.sort(key=lambda item: item[1].start_time)
		return program_list

search_menu = SearchMenu()