
from BasicClass import FacebookObject
from util import open_image, type_to_fields


class Link(FacebookObject):
    """Class to manage links, likes doesn't work somehow, managed to get those by fql'
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
        print id
        kwargs.update({"id" : id})
        self.update(kwargs)
        self.get_data()
        self._get_datE()

    def get_data(self):
        self.get_field(type_to_fields["links"])
        return self

    def get_picture(self):
        pic = open_image(self["picture"])
        self.update({"thumbnail" : pic})
        return pic

    def get_likes(self):
        def analyze_like(id):
            "A little messy, but it is necessary to make it coherent with the other stuffs"
            try:
                pic = self.fb.fql("SELECT pic_square FROM user WHERE uid = " + str(id))[0]["pic_square"]
            except Exception:
                pic = "https://fbstatic-a.akamaihd.net/rsrc.php/v2/y_/r/9myDd8iyu0B.gif"
            name = self.fb.fql("SELECT name FROM user WHERE uid = " + str(id))[0]["name"]
            return {"pic_square" : pic, "name" : name}
            
        query = "SELECT user_id FROM like WHERE object_id = " + str(self.id)
        likes = self.fb.fql(query)
        #messy too, but same good reason
        self["likes"] = {"data" : [analyze_like(like["user_id"]) for like in likes]}
        return self["likes"]["data"]
        
    def analyze(self):
        self.get_picture()
        self.get_likes()
        self.get_all_likes_comments()
        self.image_from_connection()
        self.analyze_tag()
        self.analyze_own_from()
        return self