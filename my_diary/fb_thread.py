import time
from datetime import datetime

from basic_class import FacebookObject
from util import back_dates, get_user, simple_request

import prova

def counter(f):
    def wrapper(*args):
        wrapper.count += 1
        print wrapper.count
        return f(*args)
    wrapper.count = 1
    return wrapper
    

#I believe it works, better thing to do is to don't touch it at all... 

class Fb_Thread(FacebookObject):
    def __init__(self, fb, id, kwargs={}):
        self.fb = fb
        self.id = id
        date = datetime.fromtimestamp(int(kwargs["updated_time"])).__format__("%Y-%m-%dT%H:%M:%S+0000")
        kwargs.update({"id" : id, "class" : "fb_thread", "updated_time" : date})
        self.update(kwargs)
        #self.get_data()
        self._get_datE()

    def get_data(self):
        data = self.fb.request(str(self.id))
        message = data["message"]
        date = data["updated_time"]
        starter = get_user(self.fb, data["from"]["id"])
        self.update({"updated_time" : date, "message" : message, "from" : starter})
        return self
        
   # def get_data(self):
   #     query = "SELECT updated_time, subject FROM thread WHERE thread_id = " + str(self.id)
   #     datas = self.fb.fql(query)
   #     date = datas[0]["updated_time"]
   #     date = datetime.fromtimestamp(int(date)).__format__("%Y-%m-%dT%H:%M:%S+0000")
   #     #date -> {"updated_time" : 1251265331}
   #     self.update({"updated_time" : date, "subject" : datas[0]["subject"]})
   #     return date

    @counter
    def get_message(self,  since = int(back_dates(time.time(), days = 10)), untill = int(time.time())):
        query = "SELECT body, author_id, attachment, created_time FROM message WHERE thread_id = " + str(self.id) + " and created_time > " + str(since) + " and created_time < " + str(untill) + " ORDER BY created_time ASC"
        messages = self.fb.fql(query)
        for message in messages:
            message["author"] = get_user(self.fb, message["author_id"])
        if len(messages) >= 20:
            self._get_more_message(messages, since, untill)
        self["comments"] = messages
        return messages

    @counter
    def _get_more_message(self, acc, since, untill):
        messages = acc
        while len(messages) >= 20:
            time.sleep(0.01)
            messages = sorted(messages, key = lambda k: k["created_time"])

            query = "SELECT body, created_time, author_id FROM message WHERE thread_id =  " + str(self.id)  +  "  and created_time > " + str(since)  + " and created_time < " + str(messages[-1]["created_time"])  + " ORDER BY created_time ASC"

            messages = self.fb.fql(query)
            print [x["created_time"] for x in messages]

            for message in messages:
                message["author"] = get_user(self.fb, message["author_id"])

            acc.extend(messages)
        return

    def get_message_new(self,  since = int(back_dates(time.time(), days = 10)), untill = int(time.time())):
        messages = self.fb.request(str(self.id))
        prova.i += 1
        messages["author"] = get_user(self.fb, messages["from"]["id"])
        messages["to"] = [get_user(self.fb, user["id"]) for user in messages["to"]["data"]]
        if "comments" in messages:
            for m in messages["comments"]["data"]:
                m["author"] = get_user(self.fb, m["from"]["id"])
            while time.mktime(time.strptime(messages["comments"]["data"][-1]["created_time"], "%Y-%m-%dT%H:%M:%S+0000")) > since:
                time.sleep(0.5)
                to_add = simple_request(messages["comments"]["paging"]["next"])
                prova.i += 1
                for m in to_add["data"]:
                    m["author"] = get_user(self.fb, m["from"]["id"])
                messages["comments"]["data"].extend(to_add["data"])
                if "paging" in to_add:
                    messages["comments"]["paging"] = to_add["paging"]
                else:
                    self.update(messages)
                    return
                print "\n"*5
                print to_add
                print "\n"*5
                print messages
                print prova.i
        else:
            messages["comments"] = []
            #self.update(messages)
            #return
        self.update(messages)
        return

    def analyze(self):
        self.get_message_new()

