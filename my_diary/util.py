import facebook

from tempfile import NamedTemporaryFile
from urllib2 import urlopen, HTTPError


def get_file_image(url):
    image = NamedTemporaryFile(delete=False)
    image.write(urlopen(url).read())
    image.seek(0)
    return image

class ImageFacebook(object):
    def __init__(self):
        self.images = {}

    def add_get_image(self, url):
        if not url in self.images.keys():
            self.images[url]= get_file_image(url)
        return {"url" : url, "image" : self.images[url]}

def get_user_info(fb, uid):
    user = fb.fql("select uid, name, pic_square from user where uid = " + str(uid))
    try:
        user = user[0]
    except:
        user = {}
    if "pic_square" in user and user["pic_square"]:
        user["pic_square"] = open_image(user["pic_square"])
        return user
    user["pic_square"] = open_image("https://fbstatic-a.akamaihd.net/rsrc.php/v2/y_/r/9myDd8iyu0B.gif")
    return user
    
class UserFacebook(object):
    def __init__(self):
        self.uids = {}

    def add_get_user(self, fb, uid):
        if not uid in self.uids.keys():
            self.uids[uid]= get_user_info(fb, uid)
        return self.uids[uid]
        
def simple_request(path):
    """Fetches the given path in the Graph API.
    
    We translate args to a valid query string. If post_args is
    given, we send a POST request to the given path with the given
    arguments.
    
    """
    try:
        file = urlopen(path)
    except HTTPError, e:
        response = facebook._parse_json(e.read())
        raise facebook.GraphAPIError(response)
    try:
        fileInfo = file.info()
        if fileInfo.maintype == 'text':
            response = facebook._parse_json(file.read())
        elif fileInfo.maintype == 'image':
                mimetype = fileInfo['content-type']
                response = {
                    "data": file.read(),
                    "mime-type": mimetype,
                    "url": file.url,
                }
        else:
            raise facebook.GraphAPIError('Maintype was not text or image')
    finally:
        file.close()
    if response and isinstance(response, dict) and response.get("error"):
        raise GraphAPIError(response["error"]["type"],
                            response["error"]["message"])

    return response

type_to_fields = {
    "link" : ["id","story", "message","picture","link","created_time","likes.fields(name,pic_square)","comments.fields(from,message)","description", "type"],
    "video" : ["id","story","link","picture","name", "description","likes.fields(pic_square,name)","comments.fields(message,id,from)","type","created_time"],
    "status" : ["id","story","story_tags","type","created_time", "status_type"],
    "photo" : ["id","message","story_tags","name","type","object_id","created_time","likes.fields(name,pic_square)","comments.fields(from,message)"],
    "statuses" : ["id","message","updated_time","likes.fields(id,pic_square,name)","comments.fields(message,from,created_time,like_count)", "tags", "tags", "place"],
    "swf" : ["id","story","link","picture", "name", "description","likes.fields(pic_square,name)","comments.fields(message,id,from)","type","created_time"],
    "status_like" : ["from", "name", "picture", "link"],

    #New ones
    "photos" : ["from","source","created_time","tags","comments.fields(message,id,from)","likes.fields(pic_square,name)","name"],
    "videos" : ["from","link","picture","name", "description","likes.fields(pic_square,name)","comments.fields(message,id,from)","created_time", "source", "tags"],
    "links" : ["from", "message","picture","link","created_time","comments.fields(from,message)","description",],
    "albums" : ["photos.fields(id)","id","count","created_time","likes.fields(pic_square,name)","comments", "name", "cover_photo", "place", "from",],
    "friendship" : ["story", "from", "story_tags", "created_time"],
}

def back_dates(from_epoch, days = 0):
    return from_epoch - (days * 60*60*24)

    
image = ImageFacebook()

def open_image(url):
    return image.add_get_image(url)

users = UserFacebook()
def get_user(fb, uid):
    return users.add_get_user(fb, uid)
    

def get_pic_from_uid(fb, uid, dimension = "pic_square"):
    url_pic = fb.fql("select "+ dimension +" from user where uid = " + uid)
    if len(url_pic) > 0:
        return open_image(url_pic[0]["pic_square"])
    return open_image("https://fbstatic-a.akamaihd.net/rsrc.php/v2/y_/r/9myDd8iyu0B.gif")
