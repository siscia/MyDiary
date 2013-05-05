## What is

Basic library to get data out of facebook, it manage chat messages, videos, picture, album, link, and status

## Dependencies 

The library need "facebook-skd" 
https://github.com/pythonforfacebook/facebook-sdk
You can install it using pip
``` pip install facebook-sdk```

## Basic Ideas

We have an Extractor that is a subclass of facebook.GraphAPI (main class in facebook-sdk) and a bunch of smaller class for message, videos, link, status, picture and album (subclass of BasicObject that is a subclass of dict)

The Extractor extract the data from Facebook itself, it is the only one to comunicate to the server directly.

The other classes manage the data and say what data they need.

As soon as you initialize one of the smaller class it gets some data out of facebook, in order to order those object and to make it unique.

If you need more data you need to call the method .analyze()

##How to use it

Just initialize the Extractor and then ask it what you want, if you want the video you just need to call Extractor.videos(), same for photo, message, status, etc.
The extractor will return a list of those object, you may want to call .analyze() for any of those objects.
The basic behaviour of the Extractor is to return the last 30 days of activity, so call Extractor.photo() will return the last 30 days' photo.
If you need something different you can simply change the parameter for the extractor, default parameter are:
```
since=int(back_dates(time.time(), days = 30))
untill=int(time.time())
```
who are int/floats of the timestamp you need.

To initialize the Extractor you need an Access Token, you can get it here:
https://developers.facebook.com/tools/explorer
Since it manage also "relevant" information you need to have particular permision, click to "Get Access Token" and add what it ask (try to run the extractor it will raise exception saying that you are not allow to get such information, modify the access token and iterate as long as it need)

