from datetime import datetime

import facebook
from util import simple_request, open_image, type_to_fields, get_pic_from_uid


class FacebookObject(dict):
    def __init__(self, fb, id, kwargs):
        self.fb = fb
        self.id = id
        self.update(**kwargs)

    def __eq__(self, other):
        return self.id == other.id

    def __cmp__(self, other):
        return cmp(self["date"], other["date"])

    def _get_datE(self):
        if "created_time" in self:
            date = self["created_time"]
        elif "updated_time" in self:
            date = self["updated_time"]
        elif "created" in self:
            date = self["created"]
            date = datetime.fromtimestamp(float(date))
            self.update({"date" : date})
            return date
        else:
            return
        date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S+0000")
        self.update({"date" : date})
        return date
        
    def get_field(self, field):
        fields = self.fb.request(self["id"], args = {"fields" : field})
        self.update(fields)
        return fields
        
    def get_image(self, key):
        self.update({key : open_image(self[key])})

    def image_from_connection(self):
        if "likes" in self:
            for like in self["likes"]:
                print like
                like.update({"pic_square" : open_image(like["pic_square"])})
        if "comments" in self:
            print self["comments"], self
            for comment in self["comments"]:
                print comment, "<---Comment"
                self.analyze_from(comment["from"])
                
    def all_from_paging(self, key):
        "works only with likes and data, it update the dic passed, returing only the data"
        if "next" in self[key]:
            next_pag = simple_request(self[key]["next"])
            if len(next_pag["data"]) > 0:
                self[key].update({"paging" : next_pag["paging"],
                                  "data" : key["data"].extend(next_pag["data"])})
                self.analyze_pagging(key)
        else:
            self[key] = self[key]["data"]
        return self[key]

    def get_all_likes_comments(self):
        if "likes" in self:
            self["likes"] = self.all_from_paging("likes")
        if "comments" in self:
            self["comments"] = self.all_from_paging("comments")

    def analyze_profile(self, profile_id):
        profile = self.fb.fql("select name, pic_square, url from profile where id = " + profile_id)[0]
        pic = get_pic_from_uid(self.fb, profile_id, dimension = "pic_square")
        profile.update({"pic_square" : pic})
        return profile
            
    def analyze_story_tags(self):
        if "story_tags" in self:
            print self["story"], self["story_tags"]
            tag = [t[0] for t in self["story_tags"].values()]
            for user in tag:
                user.update(self.analyze_profile(user["id"]))
            self.update({"story_tags" : tag})

    def analyze_from(self, from_dic): #Only update the image
        print from_dic["id"]
        pic = get_pic_from_uid(self.fb, from_dic["id"])
        from_dic.update({"pic_square" : pic})
        return pic

    def analyze_tag(self):
        if "tags" in self:
            self.all_from_paging("tags")
            for tag in self["tags"]:
                self.analyze_from(tag)
            return self["tags"]
    
    def analyze_own_from(self):
        if "from" in self:
            return self.analyze_from(self["from"])
            
#########################################################
##################WORKING ON PHOTO######################
#########################################################

class Photo(FacebookObject):
    def __init__(self, fb, id, kwargs={}):
        self.fb = fb
        self.id = id
        kwargs.update({"id" : id})
        self.update(kwargs)

    def get_data(self):
        self.get_field(type_to_fields["photos"])
        return self
            
    def get_photo(self):
        picture = open_image(self["source"])
        self.update({"picture" : picture})
        return picture

    def analyze(self):
        self.get_data()
        self.get_photo()
        self.get_all_likes_comments()
        self.image_from_connection()
        self.analyze_tag()
        return self

            
class Album(FacebookObject):
    def __init__(self, fb, id, kwargs={}):
        self.fb = fb
        self.id = id
        kwargs.update({"id" : id})
        self.update(kwargs)

    def get_data(self):
        self.get_field(type_to_fields["albums"])
        return self

    def analyze_single_picture(self):
        self["photos"] = [Photo(self.fb, x["id"]).analyze() for x in self["photos"]["data"]]
        return self["photos"]

    def analyze(self):
        self.get_data()
        self.analyze_single_picture()
        self.get_all_likes_comments()
        self.image_from_connection()
        self.analyze_own_from()
        return self
        
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
        kwargs.update({"id" : id})
        self.update(kwargs)

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
        #messy too, but same reason
        self["likes"] = {"data" : [analyze_like(like["user_id"]) for like in likes]}
    
        
    def analyze(self):
        self.get_data()
        self.get_picture()
        self.get_likes()
        self.get_all_likes_comments()
        self.image_from_connection()
        self.analyze_tag()
        self.analyze_own_from()
        return self