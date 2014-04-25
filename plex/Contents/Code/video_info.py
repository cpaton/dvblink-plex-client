from xml.dom.minidom import parseString
from common import DVBLinkError
from common import DVBLinkStatus
from common import string_to_bool
from constants import *

class VideoInfo(object):
    
    def __init__(self, xml_string):
        if self.from_xml__(xml_string) == False:
            raise DVBLinkError(DVBLinkStatus.STATUS_INVALID_DATA)
       
    @property    
    def name(self):
        return self.name_
    
    @property
    def description(self):
        return self.short_desc_
    
    @property    
    def subname(self):
        return self.subname_
    
    @property    
    def language(self):
        return self.language_
    
    @property    
    def actors(self):
        return self.actors_
    
    @property
    def directors(self):
        return self.directors_
    
    @property
    def writers(self):
        return self.writers_
    
    @property
    def producers(self):
        return self.producers_
    
    @property
    def guests(self):
        return self.guests_
    
    @property
    def keywords(self):
        return self.categories_
    
    @property
    def image(self):
        return self.image_

    @property
    def start_time(self):
        return self.start_time_
        
    @property    
    def duration(self):
        return self.duration_
    
    @property
    def year(self):
        return self.year_
    
    @property
    def episode_number(self):
        return self.episode_num_
    
    @property
    def season_number(self):
        return self.season_num_
    
    @property
    def stars_number(self):
        return self.stars_num_
    
    @property
    def stars_max_number(self):
        return self.starsmax_num_

    @property    
    def is_hdtv(self):
        return self.is_hdtv_
    
    @property
    def is_premiere(self):
        return self.is_premiere_
    
    @property
    def is_repeat(self):
        return self.is_repeat_     
    
    @property    
    def is_action(self):
        return self.is_action_
    
    @property
    def is_comedy(self):
        return self.is_comedy_
    
    @property
    def is_documentary(self):
        return self.is_documentary_
    
    @property
    def is_drama(self):
        return self.is_drama_
    
    @property    
    def is_educational(self):
        return self.is_educational_
    
    @property
    def is_horror(self):
        return self.is_horror_
    
    @property
    def is_kids(self):
        return self.is_kids_
    
    @property
    def is_movie(self):
        return self.is_movie_
    
    @property
    def is_music(self):
        return self.is_music_
    
    @property
    def is_news(self):
        return self.is_news_
    
    @property
    def is_reality(self):
        return self.is_reality_
    
    @property
    def is_romance(self):
        return self.is_romance_
    
    @property    
    def is_scifi(self):
        return self.is_scifi_
    
    @property
    def is_serial(self):
        return self.is_serial_
    
    @property
    def is_soap(self):
        return self.is_soap_
    
    @property
    def is_special(self):
        return self.is_special_
    
    @property    
    def is_sports(self):
        return self.is_sports_
    
    @property
    def is_thriller(self):
        return self.is_thriller_
    
    @property
    def is_adult(self):
        return self.is_adult_
                
    def from_xml__(self, xml_string):
        video_info = parseString(xml_string.encode(XMLDOC_CODEPAGE))
        try:
            self.name_ = video_info.getElementsByTagName(EPG_PROGRAM_NAME)[0].firstChild.data
        except:
            self.name_ = ""
        try:
            self.duration_ = int(video_info.getElementsByTagName(EPG_PROGRAM_DURATION)[0].firstChild.data)
        except:
            self.duration_ = 0
        try:    
            self.start_time_ = long(video_info.getElementsByTagName(EPG_PROGRAM_START_TIME)[0].firstChild.data)
        except:
            self.start_time_ = 0
        try:
            self.short_desc_ = video_info.getElementsByTagName(EPG_PROGRAM_SHORT_DESC)[0].firstChild.data
        except:
            self.short_desc_ = None
        try:
            self.subname_ = video_info.getElementsByTagName(EPG_PROGRAM_SUBNAME)[0].firstChild.data
        except:
            self.subname_ = None
        try:
            self.language_ = video_info.getElementsByTagName(EPG_PROGRAM_LANGUAGE)[0].firstChild.data
        except:
            self.language_ = None
        try:
            self.actors_ = video_info.getElementsByTagName(EPG_PROGRAM_ACTORS)[0].firstChild.data
        except:
            self.actors_ = None
        try:
            self.directors_ = video_info.getElementsByTagName(EPG_PROGRAM_DIRECTORS)[0].firstChild.data
        except:
            self.directors_ = None
        try:
            self.writers_ = video_info.getElementsByTagName(EPG_PROGRAM_WRITERS)[0].firstChild.data
        except:
            self.writers_ = None
        try:
            self.producers_ = video_info.getElementsByTagName(EPG_PROGRAM_PRODUCERS)[0].firstChild.data
        except:
            self.producers_ = None
        try:
            self.guests_ = video_info.getElementsByTagName(EPG_PROGRAM_GUESTS)[0].firstChild.data
        except:
            self.guests_ = None
        try:
            self.categories_ = video_info.getElementsByTagName(EPG_PROGRAM_CATEGORIES)[0].firstChild.data
        except:
            self.categories_ = None
        try:
            self.image_ = video_info.getElementsByTagName(EPG_PROGRAM_IMAGE)[0].firstChild.data
        except:
            self.image_ = None
        try:
            self.year_ = int(video_info.getElementsByTagName(EPG_PROGRAM_YEAR)[0].firstChild.data)
        except:
            self.year_ = 0
        try:
            self.episode_num_ = int(video_info.getElementsByTagName(EPG_PROGRAM_EPISODE_NUM)[0].firstChild.data)
        except:
            self.episode_num_ = 0
        try:
            self.season_num_ = int(video_info.getElementsByTagName(EPG_PROGRAM_SEASON_NUM)[0].firstChild.data)
        except:
            self.season_num_ = 0
        try:
            self.stars_num_ = int(video_info.getElementsByTagName(EPG_PROGRAM_STARS_NUM)[0].firstChild.data)
        except:
            self.stars_num_ = 0
        try:
            self.starsmax_num_ = int(video_info.getElementsByTagName(EPG_PROGRAM_STARSMAX_NUM)[0].firstChild.data)
        except:
            self.starsmax_num_ = 0
        try:
            self.is_hdtv_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_HDTV)[0].firstChild.data)
        except:
            self.is_hdtv_ = False
        try:
            self.is_premiere_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_PREMIERE)[0].firstChild.data)
        except:
            self.is_premiere_ = False
        try:
            self.is_repeat_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_REPEAT)[0].firstChild.data)
        except:
            self.is_repeat_ = False
        try:
            self.is_action_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_ACTION)[0].firstChild.data)
        except:
            self.is_action_ = False
        try:
            self.is_comedy_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_COMEDY)[0].firstChild.data)
        except:
            self.is_comedy_ = False
        try:
            self.is_documentary_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_DOCUMENTARY)[0].firstChild.data)
        except:
            self.is_documentary_ = False
        try:
            self.is_drama_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_DRAMA)[0].firstChild.data)
        except:
            self.is_drama_ = False
        try:
            self.is_educational_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_EDUCATIONAL)[0].firstChild.data)
        except:
            self.is_educational_ = False
        try:
            self.is_horror_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_HORROR)[0].firstChild.data)
        except:
            self.is_horror_ = False
        try:
            self.is_kids_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_KIDS)[0].firstChild.data)
        except:
            self.is_kids_ = False
        try:
            self.is_movie_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_MOVIE)[0].firstChild.data)
        except:
            self.is_movie_ = False
        try:
            self.is_music_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_MUSIC)[0].firstChild.data)
        except:
            self.is_music_ = False
        try:
            self.is_news_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_NEWS)[0].firstChild.data)
        except:
            self.is_news_ = False
        try:
            self.is_reality_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_REALITY)[0].firstChild.data)
        except:
            self.is_reality_ = False
        try:
            self.is_romance_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_ROMANCE)[0].firstChild.data)
        except:
            self.is_romance_ = False
        try:
            self.is_scifi_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_SCIFI)[0].firstChild.data)
        except:
            self.is_scifi_ = False
        try:
            self.is_serial_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_SERIAL)[0].firstChild.data)
        except:
            self.is_serial_ = False
        try:
            self.is_soap_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_SOAP)[0].firstChild.data)
        except:
            self.is_soap_ = False
        try:
            self.is_special_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_SPECIAL)[0].firstChild.data)
        except:
            self.is_special_ = False
        try:
            self.is_sports_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_SPORTS)[0].firstChild.data)
        except:
            self.is_sports_ = False
        try:
            self.is_thriller_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_THRILLER)[0].firstChild.data)
        except:
            self.is_thriller_ = False
        try:
            self.is_adult_ = string_to_bool(video_info.getElementsByTagName(EPG_PROGRAM_CAT_ADULT)[0].firstChild.data)
        except:
            self.is_adult_ = False

        return True