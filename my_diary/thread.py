import time

from basic_class import FacebookObject
from util import back_dates

#I believe it works, better thing to do is to don't touch it at all... 

class Thread(FacebookObject):
    def __init__(self, fb, id, kwargs):
        self.fb = fb
        self.id = id
        self.update(kwargs)
        self.get_data()
        self._get_datE()

    def get_message(self):
        messages = self.fb.request(str(self.id))
        self.update(messages)
        self.analyze_thread()
        return messages

    def get_data(self,  since = int(back_dates(time.time(), days = 30)), untill = int(time.time())):
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
        pass #get_data already do everything necessary
