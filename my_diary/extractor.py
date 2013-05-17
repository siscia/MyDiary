import time
import sys
from multiprocessing import Pool
from functools import partial

import facebook

from util import back_dates

def make_object(obj_to_make, q, id):
    return obj_to_make(q, id)

class Extractor(facebook.GraphAPI):
    def __init__(self, token):
        super(Extractor,self).__init__(token)

    def links(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from link import Link
        links_query = "SELECT link_id FROM link WHERE owner = me() and created_time < " + str(untill) + "and created_time > " + str(since)
        links = self.fql(links_query)
        #return Pool(processes=5).map_async(partial(make_object, Link, self), [str(link["link_id"]) for link in links])
        return [Link(self, str(link["link_id"])) for link in links]

    def albums(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from album import Album
        albums_query = "SELECT object_id FROM album WHERE owner = me() and created < " + str(untill) + "and created > " + str(since)
        albums = self.fql(albums_query)
        return Pool(processes=5).map_async(partial(make_object, Album, self), [str(album["object_id"]) for album in albums])
        #return [Album(self, str(album["object_id"])) for album in albums]

    def photo(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from photo import Photo
        my_photo_query = "SELECT object_id FROM photo WHERE owner = me() and created < " + str(untill) + "and created > " + str(since)
        tagged_p_query = "SELECT object_id FROM photo_tag WHERE subject = me() and created < " + str(untill) + "and created > " + str(since)
        my_photo = self.fql(my_photo_query)
        tagged_p = self.fql(tagged_p_query)
        all_photo = my_photo + tagged_p
        return Pool(processes=5).map_async(partial(make_object, Photo, self), [str(photo["object_id"]) for photo in all_photo])
        #return [Photo(self, str(photo["object_id"])) for photo in all_photo]

    def status(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from status import Status
        status_query = "SELECT status_id FROM status WHERE uid = me() and time < " + str(untill) + "and time > " + str(since)
        status = self.fql(status_query)
        #return Pool(processes=5).map_async(partial(make_object, Status, self), [str(statu["status_id"]) for statu in status])
        return [Status(self, str(statu["status_id"])) for statu in status]

    def thread(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from fb_thread import Fb_Thread
        threads_query = "SELECT thread_id FROM thread WHERE folder_id = 0 OR folder_id = 1 OR folder_id = 2 OR folder_id = 3 OR folder_id = 4 AND updated_time < " + str(untill) + "and updated_time > " + str(since)
        threads = self.fql(threads_query)
        return Pool(processes=5).map_async(partial(make_object, Fb_Thread, self), [str(thread["thread_id"]) for thread in threads])
        #return [Fb_Thread(self, str(thread["thread_id"])) for thread in threads]

    def videos(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        from video import Video
        my_videos_q = "SELECT vid FROM video WHERE owner = me() and created_time < " + str(untill) + "and created_time > " + str(since)
        tagged_videos_q = "SELECT vid FROM video_tag WHERE subject = me() and created_time < " + str(untill) + "and created_time > " + str(since)
        my_videos = self.fql(my_videos_q)
        tagged_videos = self.fql(tagged_videos_q)
        all_video = my_videos + tagged_videos
        return Pool(processes=5).map_async(partial(make_object, Video, self), [str(video["vid"]) for video in all_video])
        #return [Video(self, str(video["vid"])) for video in all_video]

    def new_friends(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 1000):
        from friendship import Friendship
        posts = self.request("me/posts", args = {"untill" : untill,
                                                 "since" : since,
                                                 "limit" : limit,
                                                 "fields" : ["id", "status_type"]})["data"]
        return Pool(processes=5).map_async(partial(make_object, Friendship, self), [str(p["id"]) for p in posts if "status_type" in p and p["status_type"] == "approved_friend"])
        #return [Friendship(self, str(post["id"])) for post in posts if "status_type" in post and post["status_type"] == "approved_friend"]

    def likes(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        likes_query = "select object_id from like where user_id = me()"
        likes = self.fql(likes_query)
        
