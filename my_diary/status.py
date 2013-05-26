from basic_class import FacebookObject

from util import type_to_fields

class Status(FacebookObject):
    def __init__(self, fb, id, kwargs={}):
        self.fb = fb
        self.id = id
        kwargs.update({"id" : id, "class" : "status"})
        self.update(kwargs)
        self.get_data()
        self._get_datE()

    def get_data(self):
        "Get the raw data from facebook"
        self.get_field(type_to_fields["statuses"])
        return self

    def analyze_tag(self):
        "Analyze the tag and put picture on it"
        if "tags" in self:
            self.all_from_paging("tags")
            for tag in self["tags"]:
                self.analyze_from(tag)
            return self["tags"]
        return

    def analyze(self):
        "Analyze the data returning what I need"
        if self.id != self["id"]:
            self.get_data()
            self.id = self["id"]
        self.get_all_likes_comments()
        self.image_from_connection()
        self.analyze_tag()
        return self
