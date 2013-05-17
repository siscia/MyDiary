
from basic_class import FacebookObject

from util import type_to_fields

class Friendship(FacebookObject):
    def __init__(self, fb, id, kwargs={}):
        self.fb = fb
        self.id = id
        kwargs.update({"id" : id, "class" :"friendship"})
        self.update(kwargs)
        self.get_data()
        self._get_datE()

    def get_data(self):
        self.get_field(type_to_fields["friendship"])
        return self

    def analyze(self):
        self.analyze_story_tags()
        return self
