from xml.dom.minidom import Document
from constants import *

class GenreCategoryType(object):

    ANY = 0x00000000
    NEWS = 0x00000001
    KIDS = 0x00000002
    MOVIE = 0x00000004
    SPORT = 0x00000008
    DOCUMENTARY = 0x00000010
    ACTION = 0x00000020
    COMEDY = 0x00000040
    DRAMA = 0x00000080
    EDU = 0x00000100
    HORROR = 0x00000200
    MUSIC = 0x00000400
    REALITY = 0x00000800
    ROMANCE = 0x00001000
    SCIFI = 0x00002000
    SERIAL = 0x00004000
    SOAP = 0x00008000
    SPECIAL = 0x00010000
    THRILLER = 0x00020000
    ADULT = 0x00040000
    
class EpgSearcher(object):
    
    EPG_INVALID_TIME_ = -1
    PROGRAM_COUNT_ALL_ = -1
      
    def __init__(self, **kwargs):
        kwargs.setdefault(SEARCHING_EPG_SHORT_NODE, False)
        kwargs.setdefault(SEARCHING_START_TIME_NODE, self.EPG_INVALID_TIME_)
        kwargs.setdefault(SEARCHING_END_TIME_NODE, self.EPG_INVALID_TIME_)        
        kwargs.setdefault(SEARCHING_CHANNELS_IDS_NODE, [])
        kwargs.setdefault(SEARCHING_PROGRAM_ID_NODE, None)
        kwargs.setdefault(SEARCHING_KEYWORDS_NODE, None)
        kwargs.setdefault(SEARCHING_GENRE_MASK_NODE, None)
        kwargs.setdefault(SEARCHING_COUNT_NODE, self.PROGRAM_COUNT_ALL_)

        self.is_epg_short_ = kwargs[SEARCHING_EPG_SHORT_NODE]
        self.start_time_ = kwargs[SEARCHING_START_TIME_NODE]
        self.end_time_ = kwargs[SEARCHING_END_TIME_NODE]
        self.channels_ids_ = kwargs[SEARCHING_CHANNELS_IDS_NODE]
        self.program_id_ = kwargs[SEARCHING_PROGRAM_ID_NODE]
        self.keywords_ = kwargs[SEARCHING_KEYWORDS_NODE]
        self.genre_mask_ = kwargs[SEARCHING_GENRE_MASK_NODE]
        self.requested_count_ = kwargs[SEARCHING_COUNT_NODE]
    
    def to_xml(self):
        document = Document()
        epg_searcher = document.createElementNS(XMLDOC_NAMESPACE, SEARCHING_ROOT_NODE)
        epg_searcher.setAttribute(XMLDOC_XMLNS_ATTRIBUTE, XMLDOC_NAMESPACE)
        document.appendChild(epg_searcher)        
        if self.is_epg_short_:
            epg_short = document.createElement(SEARCHING_EPG_SHORT_NODE)
            epg_searcher.appendChild(epg_short)
            epg_short.appendChild(document.createTextNode(XMLNODE_VALUE_TRUE))                    
        
        start_time = document.createElement(SEARCHING_START_TIME_NODE)
        epg_searcher.appendChild(start_time)
        start_time.appendChild(document.createTextNode(str(self.start_time_)))
        
        requested_count = document.createElement(SEARCHING_COUNT_NODE)
        epg_searcher.appendChild(requested_count)
        requested_count.appendChild(document.createTextNode(str(self.requested_count_)))
        
        end_time = document.createElement(SEARCHING_END_TIME_NODE)
        epg_searcher.appendChild(end_time)
        end_time.appendChild(document.createTextNode(str(self.end_time_)))
        
        if self.program_id_ != None:
            program_id = document.createElement(SEARCHING_PROGRAM_ID_NODE)
            epg_searcher.appendChild(program_id)
            program_id.appendChild(document.createTextNode(str(self.program_id_)))
            
        if self.keywords_ != None:
            keywords = document.createElement(SEARCHING_KEYWORDS_NODE)
            epg_searcher.appendChild(keywords)
            keywords.appendChild(document.createTextNode(self.keywords_.decode(XMLDOC_CODEPAGE)))
        
        if self.genre_mask_ != None:
            genre_mask = document.createElement(SEARCHING_GENRE_MASK_NODE)
            epg_searcher.appendChild(genre_mask)
            genre_mask.appendChild(document.createTextNode(str(self.genre_mask_)))
            
        if self.channels_ids_:
            channels_ids = document.createElement(SEARCHING_CHANNELS_IDS_NODE)
            epg_searcher.appendChild(channels_ids)
            for id in self.channels_ids_:
                id_node = document.createElement(SEARCHING_CHANNEL_ID_NODE)
                channels_ids.appendChild(id_node)
                id_node.appendChild(document.createTextNode(id))               
        return document.toxml(encoding=XMLDOC_CODEPAGE)