
from basic_class import FacebookObject
from util import open_image, type_to_fields, get_user

class Photo(FacebookObject):
    def __init__(self, fb, id, kwargs={}):
        self.fb = fb
        self.id = id
        kwargs.update({"id" : id, "class" : "photo"})
        self.update(kwargs)
        self.get_data()
        self._get_datE()

    def get_data(self):
        self.get_field(type_to_fields["photos"])
        self.update({"from" : get_user(self.fb, self["from"]["id"])})
        return self
            
    def get_photo(self):
        picture = open_image(self["source"])
        self.update({"picture" : picture})
        return picture

    def analyze(self):
        self.get_photo()
        self.get_all_likes_comments()
        self.image_from_connection()
        self.analyze_tag()
        return self
