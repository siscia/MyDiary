import time
from datetime import datetime

from basic_class import FacebookObject
from util import back_dates, get_user

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
        
    def get_message(self,  since = int(back_dates(time.time(), days = 10)), untill = int(time.time())):
        query = "SELECT body, author_id, attachment, created_time FROM message WHERE thread_id = " + str(self.id) + " and created_time > " + str(since) + " and created_time < " + str(untill) + " ORDER BY created_time ASC"
        messages = self.fb.fql(query)
        for message in messages:
            message["author"] = get_user(self.fb, message["author_id"])
        if len(messages) >= 20:
            self._get_more_message(messages, since, untill)
        self["comments"] = messages
        return messages

    def _get_more_message(self, acc, since, untill):
        message = acc
        while len(message) >= 20:
            query = "SELECT body, created_time, author_id FROM message WHERE thread_id =  " + str(self.id)  +  "  and created_time > " + str(since)  + " and created_time < " + str(message[-1]["created_time"])  + " ORDER BY created_time ASC"
            messages = self.fb.fql(query)
            for message in messages:
                message["author"] = get_user(self.fb, message["author_id"])
            acc.extend(messages)
        return 0

    def analyze(self):
        self.get_message()
