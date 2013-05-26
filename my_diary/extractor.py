import time
import sys
from multiprocessing import Pool
from functools import partial

from eventlet import spawn
import facebook

from util import back_dates

from video import Video
from link import Link
from album import Album
from photo import Photo
from status import Status
from fb_thread import Fb_Thread
from post import Post

def make_object(obj_to_make, q, id):
    return obj_to_make(q, id)

class Extractor(facebook.GraphAPI):
    def __init__(self, token):
        super(Extractor,self).__init__(token)

    def copy(self):
        return self

    def links(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        links_query = "SELECT link_id FROM link WHERE owner = me() and created_time < " + str(untill) + "and created_time > " + str(since)
        links = self.fql(links_query)
        #return [spawn(partial(make_object, Link, self), str(link["link_id"])) for link in links]
        #return Pool(processes=5).map_async(partial(make_object, Link, self), [str(link["link_id"]) for link in links])
        return [Link(self, str(link["link_id"])) for link in links]

    def albums(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        albums_query = "SELECT object_id FROM album WHERE owner = me() and created < " + str(untill) + "and created > " + str(since)
        albums = self.fql(albums_query)
        #return Pool(processes=5).map_async(partial(make_object, Album, self), [str(album["object_id"]) for album in albums])
        return [Album(self, str(album["object_id"])) for album in albums]

    def photos(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        my_photo_query = "SELECT object_id FROM photo WHERE owner = me() and created < " + str(untill) + "and created > " + str(since)
        tagged_p_query = "SELECT object_id FROM photo_tag WHERE subject = me() and created < " + str(untill) + "and created > " + str(since)
        my_photo = self.fql(my_photo_query)
        tagged_p = self.fql(tagged_p_query)
        all_photo = my_photo + tagged_p
        #return Pool(processes=5).map_async(partial(make_object, Photo, self), [str(photo["object_id"]) for photo in all_photo])
        return [Photo(self, str(photo["object_id"])) for photo in all_photo]

    def status(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        status_query = "SELECT status_id FROM status WHERE uid = me() and time < " + str(untill) + " and time > " + str(since)
        status = self.fql(status_query)
        #return Pool(processes=5).map_async(partial(make_object, Status, self), [str(statu["status_id"]) for statu in status])
        return [Status(self, str(statu["status_id"])) for statu in status]

    def threads(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        threads_query = "SELECT thread_id, updated_time FROM thread WHERE folder_id = 0 OR folder_id = 1 OR folder_id = 2 OR folder_id = 3 OR folder_id = 4 AND updated_time < " + str(untill) + "and updated_time > " + str(since)
        threads = self.fql(threads_query)
        #return Pool(processes=5).map_async(partial(make_object, Fb_Thread, self), [str(thread["thread_id"]) for thread in threads])
        return [Fb_Thread(self, str(thread["thread_id"]), thread) for thread in threads]

    def videos(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
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
        #return Pool(processes=5).map_async(partial(make_object, Friendship, self), [str(p["id"]) for p in posts if "status_type" in p and p["status_type"] == "approved_friend"])
        #return [Friendship(self, str(post["id"])) for post in posts if "status_type" in post and post["status_type"] == "approved_friend"]

    def likes(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 25):
        object_types = {"post" : Status, "link" : Link, "video" : Video, "status" : Status, "photo" : Photo, "album" : Album, "wallpost" : Status}
        likes_query = "select object_id, object_type from like where user_id = me()"
        likes = self.fql(likes_query)
        def f(l):
            print l
            try:
                return object_types[l["object_type"]](self.copy(), l["object_id"])
            except:
                return 
        likes = [f(l) for l in likes]
        return likes

    
    def posts(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), limit = 1000):
        posts = self.request("me/posts", args = {"untill" : untill,
                                                 "since" : since,
                                                 "limit" : limit,
                                                 "fields" : ["id", "type", "object_id"]})["data"]
        def make_real(post):
            if "object_id" in post:
                return Post(self.copy(), str(post["object_id"]), post["type"]).get_real()
            return Post(self.copy(), str(post["id"]), post["type"]).get_real()
        return [make_real(post) for post in posts]