from BasicClass import FacebookObject

from util import type_to_fields

class Post(FacebookObject):
    def __init__(self, fb, kwargs):
        if "id" in kwargs and "type" in kwargs:
            super(Post, self).__init__(fb, kwargs)
        else:
            raise Exception("Need id and type at least")

    def filter(self):
        if self["type"] != "status":
            return True
        else:
            if "status_type" not in self:
                self.get_field("status_type")
        if "status_type" in self and self["status_type"] == "approved_friend":
            return True
        return False

    def analyze_link(self):
        link = self.get_field(type_to_fields["link"])
        self.get_image("picture")
        self.get_all_likes_comments()
        self.image_from_connection()

    def analyze_video(self):
        video = self.get_field(type_to_fields["video"])
        self.get_image("picture")
        self.get_all_likes_comments()
        self.image_from_connection()

    def analyze_status(self):
        status = self.get_field(type_to_fields["status"])
        print "start analisis of story_tag"
        self.analyze_story_tags()
        self.get_all_likes_comments()
        self.image_from_connection()

    def analyze_swf(self):
        swf = self.get_field(type_to_fields["swf"])
        self.get_image("picture")
        self.get_all_likes_comments()
        self.image_from_connection()

    def analyze_photo(self):
        photo = self.get_field(type_to_fields["photo"])
        source = self.fb.request(photo["object_id"])["source"]
        self.update({"picture" : source}) #there is already a "picture" the one in the source is bigger, keep this in mind...
        self.get_image("picture") #that is why i did ^
        self.get_all_likes_comments()
        self.image_from_connection()

    def analyze(self):
        analyzer = {
            "link" : self.analyze_link,
            "video" : self.analyze_video,
            "status" : self.analyze_status,
            "swf" : self.analyze_swf,
            "photo" : self.analyze_photo,
        }
        analyzer[self["type"]]()