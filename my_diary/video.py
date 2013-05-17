
from util import type_to_fields, open_image
from basic_class import FacebookObject


class Video(FacebookObject):
    """Class to manage videos
    """
    def __init__(self, fb, id, kwargs={}):
        """
        Arguments:
        - `fb`: object to make fb request
        - `id`: id of the video
        - `kwargs`: start of the dictionary
        """
        self.fb = fb
        self.id = id
        kwargs.update({"id" : id, "class" :  "video"})
        self.update(kwargs)
        self.get_data()
        self._get_datE()

    def get_data(self):
        self.get_field(type_to_fields["videos"])
        return self

    def get_picture(self):
        pic = open_image(self["picture"])
        self.update({"thumbnail" : pic})
        return pic
        
    def analyze(self):
        self.get_picture()
        self.get_all_likes_comments()
        self.image_from_connection()
        self.analyze_tag()
        self.analyze_own_from()
        return self
