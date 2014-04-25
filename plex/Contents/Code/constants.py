#
# general
#
XMLDOC_CODEPAGE                    = "UTF-8"
XMLDOC_XMLNS_ATTRIBUTE             = "xmlns"
XMLDOC_NAMESPACE                   = "http://www.dvblogic.com"

XMLNODE_VALUE_TRUE                 = "true"
XMLNODE_VALUE_FALSE                = "false"

RESPONSE_ROOT_NODE                 = "response"
STATUS_CODE_NODE                   = "status_code"
XML_RESULT_NODE                    = "xml_result"

#
# recorder
#
CHANNELS_ROOT_NODE                 = "channels"
CHANNEL_ROOT_NODE                  = "channel"
CHANNEL_ID_NODE                    = "channel_id"
CHANNEL_DVBLINK_ID_NODE            = "channel_dvblink_id"
CHANNEL_NAME_NODE                  = "channel_name"
CHANNEL_NUMBER_NODE                = "channel_number"
CHANNEL_SUBNUMBER_NODE             = "channel_subnumber"
CHANNEL_TYPE_NODE                  = "channel_type"
CHANNEL_CHILD_LOCK_NODE            = "channel_child_lock"

PROGRAM_ROOT_NODE                  = "program"
PROGRAM_ID_NODE                    = "program_id"
PROGRAM_CHANNEL_ID_NODE            = CHANNEL_ID_NODE
PROGRAM_IS_SERIES_NODE             = "is_series"
PROGRAM_IS_RECORD_NODE             = "is_record"
PROGRAM_IS_REPEAT_RECORD_NODE      = "is_repeat_record"
EPG_ROOT_NODE                      = "dvblink_epg"
EPG_CHANNEL                        = "channel"
EPG_CHANNEL_NAME                   = "name"
EPG_CHANNEL_ID                     = "id"
EPG_PROGRAM                        = "program"
EPG_PROGRAM_NAME                   = "name"
EPG_PROGRAM_SHORT_DESC             = "short_desc"
EPG_PROGRAM_START_TIME             = "start_time"
EPG_PROGRAM_DURATION               = "duration"
EPG_PROGRAM_SUBNAME                = "subname"
EPG_PROGRAM_LANGUAGE               = "language"
EPG_PROGRAM_ACTORS                 = "actors"
EPG_PROGRAM_DIRECTORS              = "directors"
EPG_PROGRAM_WRITERS                = "writers"
EPG_PROGRAM_PRODUCERS              = "producers"
EPG_PROGRAM_GUESTS                 = "guests"
EPG_PROGRAM_IMAGE                  = "image"
EPG_PROGRAM_YEAR                   = "year"
EPG_PROGRAM_EPISODE_NUM            = "episode_num"
EPG_PROGRAM_SEASON_NUM             = "season_num"
EPG_PROGRAM_STARS_NUM              = "stars_num"
EPG_PROGRAM_STARSMAX_NUM           = "starsmax_num"
EPG_PROGRAM_HDTV                   = "hdtv"
EPG_PROGRAM_PREMIERE               = "premiere"
EPG_PROGRAM_REPEAT                 = "repeat"
EPG_PROGRAM_CATEGORIES             = "categories"
EPG_PROGRAM_CAT_ACTION             = "cat_action"
EPG_PROGRAM_CAT_COMEDY             = "cat_comedy"
EPG_PROGRAM_CAT_DOCUMENTARY        = "cat_documentary"
EPG_PROGRAM_CAT_DRAMA              = "cat_drama"
EPG_PROGRAM_CAT_EDUCATIONAL        = "cat_educational"
EPG_PROGRAM_CAT_HORROR             = "cat_horror"
EPG_PROGRAM_CAT_KIDS               = "cat_kids"
EPG_PROGRAM_CAT_MOVIE              = "cat_movie"
EPG_PROGRAM_CAT_MUSIC              = "cat_music"
EPG_PROGRAM_CAT_NEWS               = "cat_news"
EPG_PROGRAM_CAT_REALITY            = "cat_reality"
EPG_PROGRAM_CAT_ROMANCE            = "cat_romance"
EPG_PROGRAM_CAT_SCIFI              = "cat_scifi"
EPG_PROGRAM_CAT_SERIAL             = "cat_serial"
EPG_PROGRAM_CAT_SOAP               = "cat_soap"
EPG_PROGRAM_CAT_SPECIAL            = "cat_special"
EPG_PROGRAM_CAT_SPORTS             = "cat_sports"
EPG_PROGRAM_CAT_THRILLER           = "cat_thriller"
EPG_PROGRAM_CAT_ADULT              = "cat_adult"

SCHEDULES_ROOT_NODE                = "schedules"
SCHEDULE_ROOT_NODE                 = "schedule"
SCHEDULE_REMOVE_ROOT_NODE          = "remove_schedule"
SCHEDULE_UPDATE_ROOT_NODE          = "update_schedule"
SCHEDULE_ID_NODE                   = "schedule_id"
SCHEDULE_USER_PARAM_NODE           = "user_param"
SCHEDULE_FORCE_ADD_NODE            = "force_add"
SCHEDULE_BY_EPG_ROOT_NODE          = "by_epg"
SCHEDULE_MANUAL_ROOT_NODE          = "manual"
SCHEDULE_PROGRAM_ID_NODE           = PROGRAM_ID_NODE
SCHEDULE_CHANNEL_ID_NODE           = CHANNEL_ID_NODE
SCHEDULE_TITLE_NODE                = "title"
SCHEDULE_START_TIME_NODE           = "start_time"
SCHEDULE_DURATION_TIME_NODE        = "duration"
SCHEDULE_REPEATE_NODE              = "repeat"
SCHEDULE_DAY_MASK_NODE             = "day_mask"
SCHEDULE_NEW_ONLY_NODE             = "new_only"
SCHEDULE_SERIES_ANYTIME_NODE       = "record_series_anytime"
SCHEDULE_REC_TO_KEEP_NODE          = "recordings_to_keep"

RECORDINGS_ROOT_NODE               = "recordings"
RECORDING_ROOT_NODE                = "recording"
RECORDING_REMOVE_ROOT_NODE         = "remove_recording"
RECORDING_ID_NODE                  = "recording_id"
RECORDING_SCHEDULE_ID_NODE         = SCHEDULE_ID_NODE
RECORDING_CHANNEL_ID_NODE          = CHANNEL_ID_NODE
RECORDING_IS_ACTIVE_NODE           = "is_active"
RECORDING_IS_CONFLICT_NODE         = "is_conflict"

SEARCHING_ROOT_NODE                = "epg_searcher"
SEARCHING_CHANNEL_EPG_NODE         = "channel_epg"
SEARCHING_CHANNELS_IDS_NODE        = "channels_ids"
SEARCHING_CHANNEL_ID_NODE          = CHANNEL_ID_NODE
SEARCHING_PROGRAM_ID_NODE          = PROGRAM_ID_NODE
SEARCHING_KEYWORDS_NODE            = "keywords"
SEARCHING_GENRE_MASK_NODE          = "genre_mask"
SEARCHING_COUNT_NODE               = "requested_count"
SEARCHING_START_TIME_NODE          = "start_time"
SEARCHING_END_TIME_NODE            = "end_time"
SEARCHING_EPG_SHORT_NODE           = "epg_short"

#
# network streamer sink
#
STREAMER_ROOT_NODE                 = "stream"
STREAMER_STOP_ROOT_NODE            = "stop_stream"
STREAMER_CHANNEL_ID_NODE           = CHANNEL_DVBLINK_ID_NODE
STREAMER_PHYSICAL_CHANNEL_ID_NODE  = "physical_channel_id"
STREAMER_SOURCE_ID_NODE            = "source_id"
STREAMER_CLIENT_ID_NODE            = "client_id"
STREAMER_STREAM_TYPE_NODE          = "stream_type"
STREAMER_SERVER_ADDRESS_NODE       = "server_address"
STREAMER_CLIENT_ADDRESS_NODE       = "client_address"
STREAMER_STREAMING_PORT_NODE       = "streaming_port"
STREAMER_CHANNEL_HANDLE_NODE       = "channel_handle"
STREAMER_URL_NODE                  = "url"
STREAMER_DURATION_NODE             = "duration"

TRANSCODER_ROOT_NODE               = "trascoder"
TRANSCODER_HEIGHT_NODE             = "height"
TRANSCODER_WIDTH_NODE              = "width"
TRANSCODER_BITRATE_NODE            = "bitrate"
TRANSCODER_AUDIO_TRACK_NODE        = "audio_track"

PARENTAL_LOCK_ROOT_NODE            = "parental_lock"
PARENTAL_LOCK_CLIENT_ID_NODE       = "client_id"
PARENTAL_LOCK_CODE_NODE            = "code"
PARENTAL_LOCK_IS_ENABLE_NODE       = "is_enable"    

PARENTAL_STATUS_ROOT_NODE          = "parental_status"
PARENTAL_STATUS_IS_ENABLED_NODE    = "is_enabled"

STREAM_INFO_ROOT_NODE              = "stream_info"
STREAM_INFO_CHANNEL_ROOT_NODE      = CHANNEL_ROOT_NODE
STREAM_INFO_CLIENT_ID_NODE         = STREAMER_CLIENT_ID_NODE
STREAM_INFO_SERVER_ADDRESS_NODE    = STREAMER_SERVER_ADDRESS_NODE
STREAM_INFO_CHANNELS_IDS_NODE      = "channels_dvblink_ids"
STREAM_INFO_CHANNEL_ID_NODE        = CHANNEL_DVBLINK_ID_NODE
STREAM_INFO_CHANNEL_URL_NODE       = STREAMER_URL_NODE

#
# playback
#
OBJECT_ROOT_NODE                   = "object"
OBJECT_ID                          = "object_id"
OBJECT_ACTUAL_COUNT_NODE           = "actual_count"
OBJECT_TOTAL_COUNT_NODE            = "total_count"

CONTAINERS_ROOT_NODE               = "containers"
CONTAINER_ROOT_NODE                = "container"
CONTAINER_OBJECT_ID_NODE           = OBJECT_ID
CONTAINER_PARENT_ID_NODE           = "parent_id"
CONTAINER_NAME_NODE                = "name"
CONTAINER_DESCRIPTION_NODE         = "description"
CONTAINER_LOGO_NODE                = "logo"
CONTAINER_TYPE_NODE                = "container_type"
CONTAINER_CONTENT_TYPE_NODE        = "content_type"
CONTAINER_TOTAL_COUNT_NODE         = OBJECT_TOTAL_COUNT_NODE
CONTAINER_SOURCE_ID_NODE           = "source_id"

ITEMS_ROOT_NODE                    = "items"
ITEM_ROOT_NODE                     = "item"
ITEM_OBJECT_ID_NODE                = OBJECT_ID
ITEM_PARENT_ID_NODE                = "parent_id"
ITEM_URL_NODE                      = "url"
ITEM_THUMBNAIL_NODE                = "thumbnail"
ITEM_CAN_BE_DELETED_NODE           = "can_be_deleted"
ITEM_SIZE_NODE                     = "size"
ITEM_CREATION_TIME_NODE            = "creation_time"
    
RECORDED_TV_ROOT_NODE              = "recorded_tv"
RECORDED_TV_CHANNEL_NAME_NODE      = CHANNEL_NAME_NODE
RECORDED_TV_CHANNEL_NUMBER_NODE    = CHANNEL_NUMBER_NODE
RECORDED_TV_CHANNEL_SUBNUMBER_NODE = CHANNEL_SUBNUMBER_NODE
RECORDED_TV_STATE_NODE             = "state"

STOP_RECORDING_ROOT_NODE           = "stop_recording"
STOP_RECORDING_ID_NODE             = OBJECT_ID
        
VIDEO_ROOT_NODE                    = "video"
VIDEO_INFO_ROOT_NODE               = "video_info"
AUDIO_ROOT_NODE                    = "audio"
IMAGE_ROOT_NODE                    = "image"

OBJECT_REQUESTER_ROOT_NODE         = "object_requester"
OBJECT_REQUESTER_OBJECT_ID_NODE    = OBJECT_ID
OBJECT_REQUESTER_OBJECT_TYPE_NODE  = "object_type"
OBJECT_REQUESTER_ITEM_TYPE_NODE    = "item_type"
OBJECT_REQUESTER_POSITION_NODE     = "start_position"
OBJECT_REQUESTER_COUNT_NODE        = "requested_count"
OBJECT_REQUESTER_TYPE_NODE         = "children_request"
OBJECT_REQUESTER_SERVER_ADDR_NODE  = "server_address"

OBJECT_REMOVER_ROOT_NODE           = "object_remover"
OBJECT_REMOVER_OBJECT_ID_NODE      = OBJECT_ID