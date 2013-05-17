import time
from datetime import datetime

from basic_class import FacebookObject
from util import back_dates

#I believe it works, better thing to do is to don't touch it at all... 

class Fb_Thread(FacebookObject):
    def __init__(self, fb, id, kwargs={}):
        self.fb = fb
        self.id = id
        kwargs.update("id" : id, "class" :"fb_thread")
        self.update(kwargs)
        self.get_data()
        self._get_datE()

    def get_message(self):
        messages = self.fb.request(str(self.id))
        self.update(messages)
        self.analyze_thread()
        return messages

    def get_data(self):
        query = "SELECT updated_time FROM thread WHERE thread_id = " + str(self.id)
        date = self.fb.fql(query)[0]["updated_time"]
        date = datetime.fromtimestamp(int(date)).__format__("%Y-%m-%dT%H:%M:%S+0000")
        #date -> {"updated_time" : 1251265331}
        self.update({"updated_time" : date})
        return date
        
    def get_message(self,  since = int(back_dates(time.time(), days = 30)), untill = int(time.time())):
        query = "SELECT body, author_id, attachment, created_time FROM message WHERE thread_id = " + str(self.id) + " and created_time > " + str(since) + " and created_time < " + str(untill) + " ORDER BY created_time DESC"
        messages = self.fb.fql(query)
        print len(messages), query
        if len(messages) >= 10:
            self._get_more_message(messages, since, untill)
        self["comments"] = messages
        return messages

    def _get_more_message(self, acc, since, untill):
        message = acc
        while len(message) >= 10:
            query = "select body, created_time from message where thread_id =  " + str(self.id)  +  "  and created_time > " + str(since)  + " and created_time < " + str(message[-1]["created_time"])  + " order by created_time DESC"
            message = self.fb.fql(query)
            acc.extend(message)
            print len(message), query
        return 0

    def analyze(self):
        self.get_message()
