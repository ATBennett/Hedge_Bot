#!/usr/bin/env python
import twitter
import time
from twitter import *

#Function for obtaining the keys to an account
def authenticate():
    print "1. Create a new Twitter application here: https://apps.twitter.com"
    print "When you have created the application, enter:"
    print "   your application name: ",
    app_name = raw_input()

    print "   your consumer key: ",
    consumer_key = raw_input()

    print "   your consumer secret: ",
    consumer_secret = raw_input()

    print "2. Now, authorize this application."
    print "You'll be forwarded to a web browser in two seconds."

    time.sleep(2)

    access_key, access_secret = twitter.oauth_dance(app_name, consumer_key, consumer_secret)

    with open("config.py","r") as config_file:
        config_file_lines = config_file.readlines()

    config_file_lines[1] = "consumer_key = '" + consumer_key + "'\n"
    config_file_lines[2] = "consumer_secret = '" + consumer_secret + "'\n"
    config_file_lines[3] = "access_key = '" + access_key + "'\n"
    config_file_lines[4] = "access_secret = '" + access_secret + "'\n"
    
    with open("config.py","w") as config_file:
        for line in config_file_lines:
            config_file.write(line)

    print "Done."

#Posts an image with an optional status to twitter
def post_image(image_name, status = ''):
    config = {}
    execfile("config.py", config)
    acc_key = config["access_key"]
    acc_secret = config["access_secret"]
    con_key = config["consumer_key"]
    con_secret = config["consumer_secret"]
    twitter = Twitter(  auth = OAuth(acc_key, acc_secret, con_key, con_secret))

    imagefile = open(image_name,"rb")
    imagedata = imagefile.read()

    try:
        t_up=Twitter(domain='upload.twitter.com', auth = OAuth(acc_key, acc_secret, con_key,con_secret))
        id_img1 = t_up.media.upload(media=imagedata)["media_id_string"]
        results = twitter.statuses.update(status = status,media_ids = id_img1)
        print "Updated Status %s with file %s" % (status,image_name)

    except TwitterHTTPError:
        print "Invalid token, please run with -c argument to configure"