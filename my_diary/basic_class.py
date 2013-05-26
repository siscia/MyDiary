from datetime import datetime

import facebook
from util import simple_request, open_image, type_to_fields, get_pic_from_uid


class FacebookObject(dict):
    def __init__(self, fb, id, kwargs):
        self.fb = fb
        self.id = id
        self.update(**kwargs)

    def __eq__(self, other):
        return self["id"] == other["id"]

    def __hash__(self):
        return hash(self["id"])

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
        if key in self and "next" in self[key]:
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

class Friendship(FacebookObject):
    def __init__(self, fb, id, kwargs={}):
        self.fb = fb
        self.id = id
        kwargs.update({"id" : id})
        self.update(kwargs)
        self.get_data()
        self._get_datE()

    def get_data(self):
        self.get_field(type_to_fields["friendship"])
        return self

    def analyze(self):
        self.analyze_story_tags()
        return self