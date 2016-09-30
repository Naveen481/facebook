import os
import sys
import facebook
import json
import requests

fb_access_token = "EAACEdEose0cBACfAEZBtbKTQTZApAudwfaHuhZA0oS4CZBkeQFRHRt5NM8\
    S63bktY8LXl2OkN3ikVvXRwBiqznUQ5qMDKl2yEo42bPhGjb8jCyUtEy2ePqiR6q8SwtdSvZCj\
    1glTOZA3E8jVw7mkQHgEZCuuGhCGZCzJfWzHMAXuVwZDZD"
fb_group_id = "134244433397367"

graph = facebook.GraphAPI(fb_access_token)

def main():
    fetch_group_info()

def fetch_group_info():
    resp = graph.get_object(fb_group_id+ '?fields=feed{from}')
    feeds = resp['feed']
    members_ids = []
    while(True):
        try:
            for feed in feeds['data']:
                members_ids.append(feed['from']['id'])
                print(feed['from']['id'])
            feeds=requests.get(feed['paging']['next']).json()
        except KeyError:
            break
    
if __name__=="__main__":
    main()
