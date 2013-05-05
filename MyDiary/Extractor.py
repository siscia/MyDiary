import time

import facebook

from util import back_dates

class Extractor(facebook.GraphAPI):
    def __init__(self, token):
        super(Extractor,self).__init__(token)

    def links(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from Link import Link
        links_query = "SELECT link_id FROM link WHERE owner = me() and created_time < " + str(untill) + "and created_time > " + str(since)
        links = self.fql(links_query)
        return [Link(self, str(link["link_id"])) for link in links]

    def albums(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from Album import Album
        albums_query = "SELECT object_id FROM album WHERE owner = me() and created < " + str(untill) + "and created > " + str(since)
        albums = self.fql(albums_query)
        return [Album(self, str(album["object_id"])) for album in albums]

    def photo(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from Photo import Photo
        my_photo_query = "SELECT object_id FROM photo WHERE owner = me() and created < " + str(untill) + "and created > " + str(since)
        tagged_p_query = "SELECT object_id FROM photo_tag WHERE subject = me() and created < " + str(untill) + "and created > " + str(since)
        my_photo = self.fql(my_photo_query)
        tagged_p = self.fql(tagged_p_query)
        all_photo = my_photo + tagged_p
        return [Photo(self, str(photo["object_id"])) for photo in all_photo]

    def status(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from Status import Status
        status_query = "SELECT status_id FROM status WHERE uid = me() and time < " + str(untill) + "and time > " + str(since)
        status = self.fql(status_query)
        return [Status(self, str(statu["status_id"])) for statu in status]

    def thread(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from Fb_Thread import Fb_Thread
        threads_query = "SELECT thread_id FROM thread WHERE folder_id = 0 OR folder_id = 1 OR folder_id = 2 OR folder_id = 3 OR folder_id = 4 AND updated_time < " + str(untill) + "and updated_time > " + str(since)
        threads = self.fql(threads_query)
        return [Fb_Thread(self, str(thread["thread_id"])) for thread in threads]

    def videos(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from Video import Video
        my_videos_q = "SELECT vid FROM video WHERE owner = me() and created_time < " + str(untill) + "and created_time > " + str(since)
        tagged_videos_q = "SELECT vid FROM video_tag WHERE subject = me() and created_time < " + str(untill) + "and created_time > " + str(since)
        my_videos = self.fql(my_videos_q)
        tagged_videos = self.fql(tagged_videos_q)
        all_video = my_videos + tagged_videos
        return [Video(self, str(video["vid"])) for video in all_video]