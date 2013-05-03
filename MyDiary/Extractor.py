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