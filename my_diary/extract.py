import facebook
import time

from util import simple_request, type_to_fields, back_dates, open_image

    
class MyDiary(facebook.GraphAPI):
    def __init__(self, token):
        super(MyDiary,self).__init__(token)

    def analyze_paging(self, with_paging):
        next_pag = simple_request(with_paging["paging"]["next"])
        if len(next_pag["data"]) > 0:
            #there is somenthing next...
            with_paging.update({"paging" : next_pag["paging"],
                                "data" : with_paging["data"].extend(next_pag["data"])})
            self.analyze_pagging(with_paging)
        with_paging = with_paging["data"]
        return with_paging

    def _cycle_to_paging(self, dict_to):
        if "likes" in dict_to:
            dict_to["likes"] = self.analyze_paging(dict_to["likes"])
        if "comments" in dict_to:
            dict_to["comments"] = self.analyze_paging(dict_to["comments"])
        return 0

    def get_pic_square_from_uid(self, uid):
        url_pic = self.fql("select pic_square from user where uid = " + uid)[0]
        return open_image(url_pic["pic_square"])
        
    def get_posts_id(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), fields=[], limit = 250, to_filter=True):
        fields = fields + ["id", "type"]
        posts = self.request("me/posts", args = {"untill" : untill,
                                                 "since" : since,
                                                 "limit" : limit,
                                                 "fields" : fields})
        
        if to_filter:
            return [x for x in posts["data"] if self.filter_status(x)]
        else:
            return posts["data"]

    def get_element(self, element_id):
        return self.request(element_id)

    def get_user_picture(self, user_id, dimension="square"):
        response = self.request(user_id, args = {"fields" : ["picture.type(square)"]})
        return open_image(response["picture"]["data"]["url"])

    def get_objects_id_you_like(self):
        objects_id = self.fql("select object_id from like where user_id = me()")
        ids = [x["object_id"] for x in object_id]
        return ids

    def get_status_you_likes(self, ids, since=int(back_dates(time.time(), days = 30)), untill=int(time.time())):
        to_query = str(ids)
        to_query = list(to_query)
        to_query[0] = "("
        to_query[-1] = ")"
        to_query = "".join(to_query)
        status = self.fql("select status_id from status where status_id in " + to_query + "and time < " + str(untill) + " and time > " + str(since))
        for x in status:
            x["id"] = str(x["status_id"])
            x["type"] = "status_like"
        return status

    def analyze_status_liked(self, id):
        status = self.analyze(id, type_to_fields["status_like"])
        self.analyze_from(status)
        self.get_picture(status)
        return status
        
    def analyze(self, object_id, fields):
        return self.request(object_id, args = {"fields" : fields})
    
    def get_images(self, link_dict):
        if "picture" in link_dict:
            link_dict.update({"picture" : open_image(link_dict["picture"])})
        if "source" in link_dict:
            link_dict.update({"source" : open_image(link_dict["source"])})
        if "pic_square" in link_dict:
            link_dict.update({"pic_square" : open_image(link_dict["picture"])})
        if "likes" in link_dict:
            for a in link_dict["likes"]:  #["data"]
                a.update({"pic_square" : open_image(a["pic_square"])})
        if "comments" in link_dict:
            for a in link_dict["comments"]: #["data"]:
                a.update({"pic_square" : self.get_user_picture(a["from"]["id"], dimension = "square")})
        return link_dict
        
    def analyze_link(self, link_id):
        link = self.analyze(link_id, type_to_fields["link"])
        self._cycle_to_paging(link)
        self.get_images(link)
        return link

    def analyze_video(self, video_id):
        video = self.analyze(video_id, type_to_fields["video"])
        self._cycle_to_paging(video)
        self.get_images(video)
        return video
        
    def analyze_status(self, status_id):
        status = self.analyze(status_id, type_to_fields["status"])
        self.analyze_story_tags(status)
        return status
        
    def analyze_story_tags(self, status):
        story_tag = status["story_tags"]
        tag = [t[0] for t in story_tag.values()]
        for user in tag:
            pic = self.get_pic_square_from_uid(user["id"])
            user.update({"pic_square" : pic})
        status.update({"story_tags" : tag})
        return status
        
    def analyze_swf(self, swf_id):
        swf = self.analyze(swf_id, type_to_fields["swf"])
        self._cycle_to_paging(swf)
        self.get_images(swf)
        return swf
        
    def get_status_type(self, status_id):
        return self.analyze(status_id, ["status_type"])
        
    def filter_status(self, post):
        if post["type"] != "status":
            return True
        else:
            status = self.get_status_type(post["id"])
            if "status_type" in status and status["status_type"] == "approved_friend":
                return True
        return False
        
    def analyze_photo(self, photo_id):
        photo = self.analyze(photo_id, type_to_fields["photo"])
        source = self.request(photo["object_id"])["source"]
        photo.update({"source" : source}) #it is necessary for the get_images
        self._cycle_to_paging(photo)
        self.get_images(photo)
        return photo

    def analyze_statuses(self, statuses_id):
        statuses = self.analyze(statuses_id, type_to_fields["statuses"])
        self._cycle_to_paging(statuses)
        self.get_images(statuses)
        return statuses
        
    def get_statuses(self, since=int(back_dates(time.time(), days = 30)), untill=int(time.time()), fields = ["id"], limit = 25):
        statuses = self.request("me/statuses", args = {"fields" : fields,
                                                       "since" : since,
                                                       "untill" : untill,
                                                       "limit" :limit,})["data"]
        for state in statuses:
            state.update({"type" : "statuses", "created_time" : state["updated_time"]})
        return statuses

    def get_threads_id(self, since = int(back_dates(time.time(), days = 30)), untill = int(time.time())):
        ids = self.fql("SELECT thread_id FROM thread WHERE (folder_id = 0 or folder_id = 1 or folder_id = 4 or folder_id = 3) and updated_time < " + str(untill) + " and updated_time > " + str(since))        
        total_id = set([x['thread_id'] for x in ids])
        return total_id

    def analyze_thread(self, thread_id, since = int(back_dates(time.time(), days = 30)), untill = int(time.time())):
        query = "SELECT body, author_id, attachment, created_time FROM message WHERE thread_id = " + str(thread_id) + " and created_time > " + str(since) + " and created_time < " + str(untill) + " ORDER BY created_time DESC"
        messages = self.fql(query)
        print query
        if len(messages) >= 20:
            self._get_more_message(messages, thread_id, since, untill)
        return messages
        
    def _get_more_message(self, acc, thread_id, since, untill):
        message = acc
        while len(message) >= 20:
            message = self.fql("select body, created_time from message where thread_id =  " + str(thread_id)  +  "  and created_time > " + str(since)  + " and created_time < " + str(message[-1]["created_time"])  + " order by created_time DESC")
            acc.extend(message)
        return 0
        
    def join_list(self, first_list, *args):
        for x in args:
            first_list.extend(x)
        return first_list
        
    def sort_by_date(self, to_sort):
        to_sort.sort(key = lambda k : k['created_time'])
        return to_sort

    def analyze_from(self, with_from):
        if "from" in with_from:
            profile = self.fql("select name, pic_square, url from profile where id = " + with_from["from"]["id"])["data"]
            self.get_images(profile)
            with_from["from"].update(profile)
        else:
            raise Exception("No key 'from' in the dictionary ")
        return profile
            
    def analyze_all_post(self, posts):
        """ post -> {"type" : type, "id" : id}"""
        fun = {
            "link" : self.analyze_link,
            "video" : self.analyze_video,
            "photo" : self.analyze_photo,
            "status" : self.analyze_status,
            "statuses" : self.analyze_statuses,
            "swf" : self.analyze_swf,
        }
        for post in posts:
            yield fun[post["type"]](post["id"])
       # all_post = [ fun[post["type"]](post["id"]) for post in posts ]
       # return all_post