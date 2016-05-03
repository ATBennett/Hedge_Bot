#!/usr/bin/env python
import twitter_functions
import random
import os
import sys

def sendImages():
    random.seed()
    config = {}
    execfile("config.py", config)

    supported_file_types = ('.jpg','.gif','.png')
    DIR = config["DIR"]
    image_list = []

    #Creating a list of all the file names in DIR
    for name in os.listdir(DIR):
        file_path = os.path.join(DIR, name)
        if os.path.isfile(file_path):
            image_list.append(file_path)

    #Removing any unsupported files from the list
    for i in range(len(image_list)-1,-1,-1):
        if not image_list[i].endswith(supported_file_types):
            image_list.pop(i)

    image_list = sorted(image_list)
    message_list = config["message_strings"]

    if image_list:
        for name in config["friends"]:
            if message_list:
                message_num = random.randrange(len(message_list))

            image_num = random.randrange(len(image_list))

            string = '@'+name
            if message_list:
                string += ' ' + message_list[message_num]
            twitter_functions.post_image(image_list[image_num], string)


def main():
    args = sys.argv[1:]

    if len(args) > 1:
        print "only 1 argument alowed"
        sys.exit(1)

    if args:
        if args[0] == '-c':
            twitter_functions.authenticate()
        else:
            print "Invalid Argument, exiting"
            sys.exit(1)

    else:
            sendImages()

if __name__ == '__main__':
  main()
