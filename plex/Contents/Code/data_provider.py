import common
import datetime
import time
import helper
from http_data_provider import HttpDataProvider
from epg_searcher import EpgSearcher
from stream_info import StreamInfoRequest
from parental_lock import ParentalLock
from channels import *
from constants import *

class DataProvider(object):

	UPDATE_PERIOD_SEC_ = 0.5
	IDLE_PERIOD_SEC_ = 3600
	UPDATE_CHANNELS_AND_EPG_PERIOD_SEC_ = 43200
	UPDATE_CHANNELS_DELAY_SEC_ = 15
	UPDATE_EPG_DELAY_SEC_ = 15
	
	def init(self, app_id, address, port, user_name, password, use_cache, epg_of_days):
		helper.log_info('DataProvider.init. %s %s %s %s %s %s %s' % (app_id, address, port, user_name, password, use_cache, epg_of_days))
		self.use_cache_ = use_cache
		self.app_id_ = app_id
		self.address_ = address
		self.epg_of_days_ = epg_of_days
		self.http_data_provider_ = HttpDataProvider(address, port, user_name, password)
		self.reset_()
	
	def get_channels(self):
		if not self.channels_ or not self.use_cache_:
			self.channels_ = self.http_data_provider_.get_channels()
		return self.channels_
	
	def get_tv_channels(self):
		self.get_channels()
		return [channel for channel in self.channels_ \
			if ChannelType.CHANNEL_TV == channel.channel_type]
		
	def get_radio_channels(self):
		self.get_channels()
		return [channel for channel in self.channels_ \
			if ChannelType.CHANNEL_RADIO == channel.channel_type]
		
	def get_stream_info(self):
		if not self.channels_:
			self.channels_ = self.http_data_provider_.get_channels()
		if not self.stream_infos_ or not self.use_cache_:
			self.stream_infos_ = self.get_channels_stream_info_(self.channels_)
		return dict((stream_info.dvblink_channel_id, stream_info.channel_url) \
			for stream_info in self.stream_infos_)
    
	def get_channel_epg(self, channel_id):
		if self.channels_id_with_programs_dict_.has_key(channel_id):
			return self.channels_id_with_programs_dict_[channel_id]
		else:
			programs = self.search_epg_(channel_id)
			if self.use_cache_:
				self.channels_id_with_programs_dict_[channel_id] = programs
			return programs
			
	def get_actual_programs(self, requested_count):
		if self.is_update_completed_ and self.use_cache_:
			return self.get_actual_programs_locally_(requested_count)
		else:
			return self.get_actual_programs_remotely_(requested_count)
    
	def search_epg_by_keywords(self, keywords):
		searcher = EpgSearcher(keywords=keywords)
		return self.http_data_provider_.search_epg(searcher)
		
	def search_epg_by_genre(self, genre_mask):
		searcher = EpgSearcher(genre_mask=genre_mask)
		return self.http_data_provider_.search_epg(searcher)
	
	def play_channel(self, request_stream):
		return self.http_data_provider_.play_channel(request_stream)
		
	def stop_channel(self, stop_stream):
		return self.http_data_provider_.stop_channel(stop_stream)
	
	def get_recordings(self, is_forced = True):
		if is_forced or self.recordings_ == None or not self.use_cache_:
			self.recordings_ = self.http_data_provider_.get_recordings()
		return self.recordings_
	
	def get_schedules(self):
		return self.http_data_provider_.get_schedules()
	
	def add_schedule(self, schedule):
		return self.http_data_provider_.add_schedule(schedule)
		
	def update_schedule(self, schedule_updater):
		return self.http_data_provider_.update_schedule(schedule_updater)
	
	def remove_schedule(self, schedule_remover):
		return self.http_data_provider_.remove_schedule(schedule_remover)
	
	def remove_recording(self, recording_remover):
		return self.http_data_provider_.remove_recording(recording_remover)
	
	def get_object(self, object_requester):
		return self.http_data_provider_.get_object(object_requester)
	
	def remove_object(self, object_remover):
		return self.http_data_provider_.remove_object(object_remover)
	
	def stop_recording(self, stop_recording):
		return self.http_data_provider_.stop_recording(stop_recording)
	
	def set_parental_lock(self):
		parental_lock = ParentalLock(client_id=self.app_id_, is_enable=True)
		return self.http_data_provider_.set_parental_lock(parental_lock)
	
	def reset_parental_lock(self, lock_code):
		parental_lock = ParentalLock(client_id=self.app_id_, is_enable=False, code=lock_code)
		return self.http_data_provider_.set_parental_lock(parental_lock)
		
	def schedule_processing(self):
		if (long(time.time()) - self.last_channels_update_) > self.UPDATE_CHANNELS_AND_EPG_PERIOD_SEC_:
			try:
				self.channels_ = self.http_data_provider_.get_channels()
				self.stream_infos_ = self.get_channels_stream_info_(self.channels_)
				if not self.channels_ or not self.stream_infos_:
					raise Exception()
				self.recordings_ = self.http_data_provider_.get_recordings()
				self.channels_without_epg_ = self.channels_[:]
				self.last_channels_update_ = long(time.time())
			except:
				self.last_channels_update_ = long(time.time()) - self.UPDATE_CHANNELS_AND_EPG_PERIOD_SEC_ + self.UPDATE_CHANNELS_DELAY_SEC_
		else:
			if self.channels_without_epg_ and ((long(time.time()) - self.last_error_time_) > self.UPDATE_EPG_DELAY_SEC_):
				try:
					channel = self.channels_without_epg_[0]
					self.channels_id_with_programs_dict_[channel.channel_id] = self.search_epg_(channel.channel_id)
					del self.channels_without_epg_[0]
					if not len(self.channels_without_epg_):
						self.is_update_completed_ = True
						return self.IDLE_PERIOD_SEC_
				except Exception, error:
					self.last_error_time_ = long(time.time())
		return self.UPDATE_PERIOD_SEC_
	
	def search_epg_(self, channel_id):
		time_now = datetime.datetime.now()
		start_time = common.datetime_to_ctime(time_now)
		end_time = common.datetime_to_ctime(time_now + datetime.timedelta(days=self.epg_of_days_))
		searcher = EpgSearcher(channels_ids=[channel_id], start_time=start_time, end_time=end_time)
		return self.http_data_provider_.search_epg(searcher)
	
	def get_channels_stream_info_(self, channels):
		channels_ids = []
		for channel in channels:
			channels_ids.append(channel.dvblink_channel_id)
		if channels_ids:
			stream_info = StreamInfoRequest(self.address_, self.app_id_, channels_ids)
			return self.http_data_provider_.get_stream_info(stream_info)
		return []
	
	def get_actual_programs_locally_(self, requested_count):
		channels_epg_dict = {}
		time_now = common.datetime_to_ctime(datetime.datetime.now())
		for channel_id, program_dict in self.channels_id_with_programs_dict_.items():
			try:
				program_list = program_dict.get(channel_id, None)
				current_program_list = []
				for program in program_list:
					if time_now < (program.start_time + program.duration):
						current_program_list.append(program)
					if len(current_program_list) == requested_count:
						break
				channels_epg_dict[channel_id] = current_program_list
			except:
				pass
		return channels_epg_dict
	
	def get_actual_programs_remotely_(self, requsted_count):
		time_now = datetime.datetime.now()
		start_time = common.datetime_to_ctime(time_now)
		end_time = common.datetime_to_ctime(time_now + datetime.timedelta(days=1))
		searcher = EpgSearcher(start_time=start_time, end_time=end_time, requested_count=requsted_count, epg_short=True)
		return self.http_data_provider_.search_epg(searcher)
	
	def reset_(self):
		self.channels_ = []
		self.recordings_ = None
		self.stream_infos_ = []
		self.channels_without_epg_ = []
		self.channels_id_with_programs_dict_ = {}
		self.is_update_completed_ = False
		self.last_channels_update_ = 0
		self.last_error_time_ = 0
        
data_provider = DataProvider()