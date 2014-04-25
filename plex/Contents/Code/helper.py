import common
from localization import *

SERVER_PORT_DEFAULT_VALUE = 8080
EPG_OF_DAYS_DEFAULT_VALUE = 4
MIN_SERVER_PORT = 1
MAX_SERVER_PORT = 65535
MAX_HALF_STARS = 10

SERVER_ADDRESS_KEY = "address"
SERVER_PORT_KEY = "port"
USER_NAME_KEY = "user_name"
PASSWORD_KEY = "password"
CHANNEL_SORT_MODE_KEY = "sort_mode"
EPG_OF_DAYS_ID_KEY = "epg_of_days"
PLUGIN_UUID_KEY = "plugin_id"

ART_PLUGIN = "art-default.jpg"
ART_TV_CHANNELS = "art_tv_channels.jpg"
ART_RADIO_CHANNELS = "art_radio_channels.jpg"
ART_RECORDED_TV = "art_recorded_tv.jpg"
ART_SETTINGS = "art_settings.jpg"
ART_TV_GUIDE = "art_tv_guide.jpg"
ART_SCHEDULED_RECORDINGS = "art_scheduled_recordings.jpg"
ART_SEARCH = "art_search.jpg"

ICON_PLUGIN = "icon-default.png"
ICON_TV_CHANNELS = "icon_tv_channels.png"
ICON_RADIO_CHANNELS = "icon_radio_channels.png"
ICON_RECORDED_TV = "icon_recorded_tv.png"
ICON_SETTINGS = "icon_settings.png"
ICON_TV_GUIDE = "icon_tv_guide.png"
ICON_TV_CHANNEL = "icon_tv_channel.png"
ICON_RADIO_CHANNEL = "icon_radio_channel.png"
ICON_TV_GUIDE_CHANNEL = "icon_tv_guide_channel.png"
ICON_SCHEDULED_RECORDINGS = "icon_scheduled_recordings.png"
ICON_SEARCH = "icon_search.png"
ICON_ADD_RECORDING = "icon_add_recording.png"
ICON_ADD_SERIES = "icon_add_series.png"
ICON_CANCEL_RECORDING = "icon_cancel_recording.png"
ICON_CANCEL_SERIES = "icon_cancel_series.png"
ICON_KEYWORD = "icon_keyword.png"
ICON_CATEGORIES = "icon_categories.png"

epg_of_days_dict = {
	str(IDS_EPG_2_DAY): 2,
	str(IDS_EPG_3_DAY): 3,
	str(IDS_EPG_4_DAY): 4,
	str(IDS_EPG_5_DAYS): 5,
	str(IDS_EPG_6_DAYS): 6,
	str(IDS_EPG_7_DAYS): 7
}

#
# Enums
#
class SortMode(object):
    BY_NAME = 0
    BY_NUMBER = 1

#
# global functions
#
def get_status_string_id(dvblink_error):
    return {
        common.DVBLinkStatus.STATUS_OK: IDS_SUCCESS_MSG,
        common.DVBLinkStatus.STATUS_NOT_IMPLEMENTED: IDS_COMMAND_NOT_IMPLEMENTED_MSG,
        common.DVBLinkStatus.STATUS_MC_NOT_RUNNING: IDS_MC_NOT_RUNNING_MSG,
        common.DVBLinkStatus.STATUS_MCE_CONNECTION_ERROR: IDS_MC_CONNECTION_ERROR_MSG,
        common.DVBLinkStatus.STATUS_INVALID_DATA: IDS_INVALID_DATA_MSG,
        common.DVBLinkStatus.STATUS_CONNECTION_ERROR: IDS_DVBLINK_CONNECTION_ERROR_MSG,
        common.DVBLinkStatus.STATUS_NO_DEFAULT_RECORDER: IDS_NO_DEFAULT_RECORDER_MSG,
        common.DVBLinkStatus.STATUS_UNAUTHORISED: IDS_UNAUTHORISED_ERROR_MSG,
        common.DVBLinkStatus.STATUS_ERROR: IDS_GENERAL_ERROR_MSG,
        common.DVBLinkStatus.STATUS_INVALID_PARAM: IDS_INVALID_PARAM_MSG
    }.get(dvblink_error.value, IDS_UNKNOWN_MSG)
	
def log_info(string):
    Log.Info("DVBLink Client: %s" % string)

def log_error(string, trace=True):
    Log.Error("DVBLink Client: %s" % string)

def calculate_rating(stars_number, stars_max):
	if stars_max and stars_number:
		return MAX_HALF_STARS / float(stars_max) * stars_number
	return stars_number

def create_program_title(program, is_record, is_series_record, is_conflicting):
	title = "%s  %s" % (common.get_time(program.start_time), create_recording_title(program, is_record, is_series_record, is_conflicting))
	return title

def create_recording_title(program, is_record, is_series_record, is_conflicting):
	title = ""
	if is_conflicting:
		title += "[%s] " % IDS_CONFLICT_RECORDING_LABEL
	elif is_series_record:
		title += "[%s] " % IDS_SERIES_RECORD_LABEL
	elif is_record:
		title += "[%s] " % IDS_RECORD_LABEL
	elif common.is_current_program(program):
		title += "[%s] " % IDS_NOW_LABEL
	title += "%s" % program.name
	return title
	
def create_program_summary(program):
	summary = "%s, %s - %s\n\n%s" % (
		IDS_TODAY_LABEL if common.is_time_today(program.start_time) else common.get_date(program.start_time),
		common.get_time(program.start_time),
		common.get_time(program.start_time + program.duration),
		create_summary(program))
	return summary
		
def create_summary(video_info):
	summary = ""
	if video_info.subname:
		summary += "%s\n\n" % create_series_info(video_info)
	if video_info.description:
		summary += "%s\n\n" % video_info.description
	if video_info.keywords:
		summary += "%s\n\n" % video_info.keywords.replace("/", ", ")
	casts = create_cast_and_crew(video_info)
	if casts:
		summary += "%s\n\n" % casts
	if video_info.year:
		summary += "%s: %d" % (IDS_YEAR_HEADER, video_info.year)
	return summary
	
def create_series_info(video_info):
	series_info = ""
	if video_info.subname:
		series_info = video_info.subname + "  "
		if video_info.episode_number or video_info.season_number:
			series_info += "("
			if video_info.episode_number:
				series_info += IDS_EPISODE_LABEL + " " + str(video_info.episode_number)
				if video_info.season_number:
					series_info += " / "
			if video_info.season_number:
				series_info += IDS_SEASON_LABEL + " " + str(video_info.season_number)
			series_info += ")"
	return series_info
	
def create_cast_and_crew(video_info):       
	label_formatted = ""
	if video_info.actors:
		label_formatted += "%s: %s" % (IDS_ACTORS_HEADER, video_info.actors.replace("/", ", "))
	if video_info.directors:
		label_formatted += "\n%s: %s" % (IDS_DIRECTORS_HEADER, video_info.directors.replace("/", ", "))
	if video_info.producers:
		label_formatted += "\n%s: %s" % (IDS_PRODUCERS_HEADER, video_info.producers.replace("/", ", "))
	if video_info.guests:
		label_formatted += "\n%s: %s" % (IDS_GUESTS_HEADER, video_info.guests.replace("/", ", "))
	if video_info.writers:
		label_formatted += "\n%s: %s" % (IDS_WRITERS_HEADER, video_info.writers.replace("/", ", "))
	return label_formatted
	
def get_epg_of_days(value):
	return epg_of_days_dict.get(value, EPG_OF_DAYS_DEFAULT_VALUE)