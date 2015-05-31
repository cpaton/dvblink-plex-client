import helper
import common
from data_provider import data_provider
from object import *
from localization import *
from constants import *

class RecordedTVMenu(object):

	DLRECORDER_SOURCE_ID_ = "8F94B459-EFC0-4D91-9B29-EC3D72E92677"

	def create(self):
		try:
			categories = self.get_recorder_categories_()
			if categories:
				return self.create_category_menu_(categories)
			else:
				return MessageContainer(
					header=IDS_CAPTION_WARNING,
					message=IDS_RECORDER_NOT_FOUND_MSG)
		except common.DVBLinkError, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=helper.get_status_string_id(error))
		except Exception, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=str(error))

	def create_recorded_tv_list(self, title, object_id):
		try:
			oc = ObjectContainer(
				no_history = True,
				no_cache = True,
				title1 = IDS_RECORDED_TV_MENU_ITEM,
				title2 = title,
				art = R(helper.ART_RECORDED_TV))
			object = self.get_object_(object_id)
			if object.containers and len(object.containers):
				for container in object.containers:
					container_object = self.create_recorded_tv_container_(container)
					oc.add(container_object)
			if object.items and len(object.items):
				for item in object.items:
					item_object = self.create_recorded_tv_item(
						item.url,
						item.object_id,
						item.recording_title,
						item.channel_name,
						helper.create_summary(item.video_info),
						float(helper.calculate_rating(item.video_info.stars_number, item.video_info.stars_max_number)),
						item.video_info.start_time,
						item.video_info.duration * 1000,
						item.video_info.year,
						item.video_info.writers.split('/') if item.video_info.writers else [],
						item.video_info.directors.split('/') if item.video_info.directors else [],
						item.video_info.producers.split('/') if item.video_info.producers else [],
						item.video_info.guests.split('/') if item.video_info.guests else [],
						item.video_info.keywords.split('/') if item.video_info.keywords else [],
						item.thumbnail
					)
					oc.add(item_object)
			return oc
		except common.DVBLinkError, error:
			return MessageContainer(
				header=IDS_CAPTION_ERROR,
				message=helper.get_status_string_id(error))

	def create_recorded_tv_item(self, url, object_id, title, source_title, summary, rating, start_time, duration, year, writers, directors, producers, guests, genres, thumbnail, include_container=False):
		item_object = VideoClipObject(
			key = Callback(
				self.create_recorded_tv_item,
				url = url,
				object_id = object_id,
				title = title,
				source_title = source_title,
				summary = summary,
				rating = rating,
				start_time = start_time,
				duration = duration,
				year = year,
				writers = writers,
				directors = directors,
				producers = producers,
				guests = guests,
				genres = genres,
				thumbnail = thumbnail,
				include_container = True
			),
			rating_key = object_id,
			title = title,
			source_title = source_title,
			summary = summary,
			rating = rating,
			originally_available_at = Datetime.FromTimestamp(start_time).date(),
			duration = duration,
			year = year,
			writers = writers,
			directors = directors,
			producers = producers,
			genres = genres,
			thumb = Resource.ContentsOfURLWithFallback(thumbnail),
			items = [
				MediaObject(
					parts = [
						PartObject(key=Callback(self.play_recording, url=url))
					]
				)
			]
		)

		if include_container:
			return ObjectContainer(objects=[item_object])
		else:
			return item_object

	def play_recording(self, url):
		return Redirect(url)

	def create_category_menu_(self, categories):
		oc = ObjectContainer(
			no_history = True,
			no_cache = True,
			title2=IDS_RECORDED_TV_MENU_ITEM,
			art = R(helper.ART_RECORDED_TV))
		for index, category in enumerate(categories):
			oc.add(DirectoryObject(
				key = Callback(self.create_recorded_tv_list, title=category.name, object_id=category.object_id),
				title = category.name,
				summary = category.description,
				thumb = Resource.ContentsOfURLWithFallback(category.logotype)))
		return oc

	def create_recorded_tv_container_(self, container):
		container_object = DirectoryObject(
			key = Callback(self.create_recorded_tv_list, title=container.name, object_id=container.object_id),
			title = container.name,
			summary = container.description,
			thumb = Resource.ContentsOfURLWithFallback(container.logotype))
		return container_object

	def get_recorder_categories_(self):
		category_list = None
		object = self.get_object_(ObjectRequester.OBJECT_ROOT_ID)
		if object.containers and len(object.containers):
			for container in object.containers:
				if self.DLRECORDER_SOURCE_ID_ == container.source_id:
					object = self.get_object_(container.object_id)
					category_list = object.containers
		return category_list

	def get_object_(self, object_id):
		object_requester = ObjectRequester(object_id=object_id,
			server_address=Prefs[helper.SERVER_ADDRESS_KEY])
		return data_provider.get_object(object_requester)

recorded_tv_menu = RecordedTVMenu()
