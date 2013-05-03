import unittest
from tempfile import NamedTemporaryFile

from info import api_key

from MyDiary.extract import MyDiary
from MyDiary.Album import Album
from MyDiary.Photo import Photo

class AlbumTest(unittest.TestCase):
    def setUp(self):
        self.q = MyDiary(api_key)
        self.album = Album(self.q, "531705626879819")
        self.album.analyze()

    def test_name(self):
        self.assertEqual(self.album["name"], "Prova MyDiary")

    def test_key(self):
        keys = self.album.keys()
        keys = set(keys)
        necessary = set(["date", "id", "name", "photos"])
        self.assertTrue(necessary.issubset(keys))

    def test_photo(self):
        photos = self.album["photos"]
        for photo in photos:
            self.assertEqual(type(photo), Photo)

    def test_comments(self):
        if "comments" in self.album:
            comments = self.album["comments"]
            for comment in comments:
                self.assertEqual(type(comment), dict)
                self.assertTrue("from" in comment)
                self.assertTrue("message" in comment)
                self.assertTrue("id" in comment)
                self.assertEqual(type(comment["from"]["pic_square"].file), file)

    def test_likes(self):
        likes = self.album["likes"]
        for like in likes:
            self.assertEqual(type(like), dict)
            self.assertTrue("name" in like)
            self.assertTrue("id" in like)
            self.assertEqual(type(like["pic_square"].file), file)


class PhotoTest(unittest.TestCase):
    def setUp(self):
        self.q = MyDiary(api_key)
        self.photos = [Photo(self.q,x).analyze() for x in ["10200923835488068", "10200907487559380", "535473603158881", "10151730937928084"]]

    def test_keys(self):
        necessary = set(["source", "picture", "from",])
        for photo in self.photos:
            keys = set(photo.keys())
            self.assertTrue(necessary.issubset(keys))

    def test_likes(self):
        for photo in self.photos:
            if "likes" in photo:
                for like in photo["likes"]:
                    self.assertEqual(type(like["pic_square"].file), file)
                    self.assertTrue("name" in like)
                    self.assertTrue("id" in like)

    def test_comments(self):
        for photo in self.photos:
            if "comments" in photo:
                for comment in photo["comments"]:
                    self.assertEqual(type(comment), dict)
                    self.assertTrue("from" in comment)
                    self.assertTrue("message" in comment)
                    self.assertTrue("id" in comment)
                    self.assertEqual(type(comment["from"]["pic_square"].file), file)
            
    def test_order_picture(self):
        ordered = sorted(self.photos)
        for i in xrange(len(self.photos)-1):
            self.assertLess(ordered[i]["date"], ordered[i+1]["date"])

    def test_all_different_but_one(self):
        for i in xrange(len(self.photos)-1):
            self.assertNotEqual(self.photos[i], self.photos[i+1])
        class Trivial(object):
            def __init__(self, id):
                self.id = id
        self.assertEqual(self.photos[0], Trivial("10200923835488068")) #this is a bug with a suit

    
if __name__ == '__main__':
    unittest.main()
