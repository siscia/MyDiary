from basic_class import FacebookObject

from video import Video
from link import Link
from album import Album
from photo import Photo
from status import Status

class Post(FacebookObject):
    def __init__(self, fb, id, type_p, kwargs={}):
        self.id = id
        self.fb = fb
        self.type_p = type_p

    def get_real(self):
        possible_types = {
            "link" : Link,
            "status" : Status,
            "photo" : Photo,
            "video" : Video,
            "album" : Album,
            "swf" : Link,            
        }
        if self.type_p in possible_types:
            return possible_types[self.type_p](self.fb.copy(), self.id)
        else:
            return self.type_p