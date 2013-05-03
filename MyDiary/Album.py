
from BasicClass import FacebookObject
from Photo import Photo

from util import type_to_fields

class Album(FacebookObject):
    def __init__(self, fb, id, kwargs={}):
        self.fb = fb
        self.id = id
        kwargs.update({"id" : id})
        self.update(kwargs)
        self.get_data()
        self._get_datE()

    def get_data(self):
        self.get_field(type_to_fields["albums"])
        return self

    def analyze_single_picture(self):
        self["photos"] = [Photo(self.fb, x["id"]).analyze() for x in self["photos"]["data"]]
        return self["photos"]

    def analyze(self):
        self.analyze_single_picture()
        self.get_all_likes_comments()
        self.image_from_connection()
        self.analyze_own_from()
        return self