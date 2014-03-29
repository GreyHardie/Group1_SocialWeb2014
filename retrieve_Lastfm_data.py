# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 00:57:36 2014

@author: Group 1 - Social Web 2014
"""
import pylast
import os, json
from datetime import date

debug = True

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account for Last.fm
API_KEY = "36b0f2c10e283a69776927c6f254a38f" # this is a sample key
API_SECRET = "db21e9c76bf1cbb460d60329fdaefa11"

# In order to perform a write operation you need to authenticate yourself
username = "user_account_name"
password_hash = "3f08c1696d7ac30a0253682ce7e192f5"

if (debug): print "Creating connection to Last.fm...\n"

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = 
    API_SECRET, username = username, password_hash = password_hash)

# The user accounts that we want collect information on

test_user = "GiPPe";

if (debug): print "Retrieving Last.fm data for user: {0} \n".format(test_user)

user_data = {"name": test_user , "fav_tracks" : [], "recent_tracks" : [], "recent_time": [], "recent_date" : [], "top_tracks": [], "top_tracks_weight" :[]}

user = network.get_user(test_user)

if (debug): print "Retrieving loved tracks...."
#get 100 favourite "loved" songs of user
loved_tracks = user.get_loved_tracks(100)

#extract track details from lastfm data
for track in loved_tracks:
    track_artist = str(track.track)
    user_data["fav_tracks"].append(track_artist)
    
#    if we want to split the artist from the track details    
#    track_artist = str(track.track).split(" - ")
#    user_data["top_tracks"].append({"atrist" : track_artist[0], "title" : track_artist[1]})
if (debug): print "Complete! Retrieved {0} tracks\n".format(len(user_data["fav_tracks"]))

if (debug): print "Retrieving top tracks from last 3 months"   
top_tracks = user.get_top_tracks(pylast.PERIOD_3MONTHS)
#extract track details from lastfm data
for track in top_tracks:
    track_artist = str(track.item)
    weight = int(track.weight)
    user_data["top_tracks"].append(track_artist)
    user_data["top_tracks_weight"].append(weight)
    
if (debug): print "Complete! Retrieved {0} tracks\n".format(len(user_data["top_tracks"]))


if (debug): print "Retrieving last months tracks listened to"    
#get the most recently played 200 songs from the last month (the limit seems to be 200) (limit = None causes script to hang and crash)
recent_tracks = user.get_recent_tracks(200)

today = date.today();

for track in recent_tracks:
    track_artist = str(track.track)
    play_date = str(track.playback_date)
    play_time = int(track.timestamp)  
    trackdate = date.fromtimestamp(play_time) #check that the song was played within the time period of interest
    delta = today - trackdate;
    if delta.days < 30 : #limit to only the last month
        user_data["recent_tracks"].append(track_artist)
        user_data["recent_time"].append(play_time)
        user_data["recent_date"].append(play_date)
        

if (debug): print "Complete! Retrieved {0} tracks\n".format(len(user_data["recent_tracks"]))       

#directory name to store the user data in
directory = 'collected_data'

if (debug): print "Writing data to file: "+'{0}/lastfm_data.json'.format(directory)
#check if directory exists if not then make it
if not os.path.exists(directory):
    os.makedirs(directory)

with open('{0}/lastfm_data.json'.format(directory), 'w') as outfile:
    json.dump(user_data, outfile, indent = 4)
    
if (debug): print "Finished!" 


