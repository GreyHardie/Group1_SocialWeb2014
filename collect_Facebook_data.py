# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 22:24:22 2014

@author: Group 1 - Social Web 2014
"""

import facebook #facebook sdk
import os,json
import calendar
from datetime import datetime,timedelta

debug = True

#user token needs permissions ....
token = 'CAACEdEose0cBAHw0q4r2oO0MpTxShpeBeQb7npDti1NZBQXSSaMEkX96a5UXk35IZCN54lAFFEoPc9tpYNZBdedHjjs1UpetlDU2HcBSPRBvSRSm7Jbs4JjKuKewrdkFGyBmZBOUl7XvDlx2X3qJnKD0oqWBg6ztkGm1SXoWfooR05zGn7i8kOuDgfOCnIXrZCENy4yEkygZDZD'
# Create a connection to the Graph API with your access token
fb = facebook.GraphAPI(token);

#get user info (id, name, photo..small)
user = fb.get_object('me');
user_pic = fb.get_connections('me','picture')["url"];

if (debug): print "Retrieving Facebook data for user: {0} \n".format(str(user["name"]))

#object to store all the data
user_data = {"name": user["name"],"pic":user_pic, "id": user["id"], "statuses" : [], "status_dates" : [], "posts": [], "post_dates" : [], "f_statuses": [], "f_dates" :[], "liked":[], "f_ids":[], "f_pics":[], "f_names":[]}

#calculate the timestamp for 30days ago
today = datetime.today()
time_period = timedelta(days=30)
start_date = today - time_period
start_timestamp = calendar.timegm(start_date.utctimetuple())

if (debug): print "Retrieving Facebook status updates for user"
   
#get user status updates (last month)
user_statuses = fb.get_connections(user["id"], 'statuses',since=start_timestamp)['data'];
for status in user_statuses:
    if status.get('message'):
        user_data["statuses"].append(str(status['message']))
        user_data["status_dates"].append(str(status['updated_time']))
        
if (debug): print "Complete! Retrieved {0} updates\n".format(len(user_data["statuses"]))

if (debug): print "Retrieving Facebook posts"

#get user posts (last month)
user_posts = fb.get_connections('me', 'posts',since=start_timestamp)['data'];
for post in user_posts:
    if post.get('message'):
        user_data["statuses"].append(str(post['message']))
        user_data["status_dates"].append(str(post['updated_time']))

if (debug): print "Complete! Retrieved {0} posts\n".format(len(user_data["posts"]))

if (debug): print "Retrieving Facebook friends info and status updates"
    
#get user friends details (id, name, photo)
#get friends status updates that user liked (in last month)
friends = fb.get_connections('me', 'friends') ['data'];

for friend in friends:
    f_id = friend["id"]
    f_name = friend["name"]
    f_pic = fb.get_connections(f_id,'picture')["url"]
    statuses = fb.get_connections(f_id,'statuses', since=start_timestamp)['data'];
    for status in statuses:
        if status.get('message'):
            user_data["f_ids"].append(str(f_id))
            user_data["f_names"].append(str(f_name))
            user_data["f_pics"].append(str(f_pic))
            user_data["f_statuses"].append(str(status['message']))
            user_data["f_dates"].append(str(status['updated_time']))
            liked = False
            if status.get('likes'):
                for like in (status['likes']['data']):
                    if str(like["id"]) == str(user["id"]):
                        liked = True
                        print "liked"
            user_data["liked"].append(liked)
            
if (debug): print "Complete! Retrieved {0} friend updates from {1} friends\n".format(len(user_data["f_statuses"]),len(friends))

#do some basic cleaning of messages (remove newlines and html)

#save info to file
#directory name to store the user data in
directory = 'collected_data'

if (debug): print "Writing data to file: "+'{0}/facebook_data_{1}.json'.format(directory,user_data["name"])

#check if directory exists if not then make it
if not os.path.exists(directory):
    os.makedirs(directory)

with open('{0}/facebook_data_{1}.json'.format(directory,user_data["name"]), 'w') as outfile:
    json.dump(user_data, outfile, indent = 4)
    
if (debug): print "Finished!" 



