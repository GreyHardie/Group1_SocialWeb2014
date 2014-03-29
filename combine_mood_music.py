# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 22:24:22 2014

@author: Group 1 - Social Web 2014
"""
import os,json
from collections import Counter
from datetime import datetime,timedelta

#verbose mode
debug = True

#directions to where the data file is stored
directory = "collected_data/"
user_file_senti = "sentiment_data_Viola Pinzi.json"
user_file_lastfm = "lastfm_data_GiPPe.json"

if (debug): print "Loading user Facebook status sentiment data from JSON file"

with open(directory+user_file_senti) as json_file:
    user_data = json.load(json_file)

if (debug): print "Loading user Lastfm data from JSON file"

with open(directory+user_file_lastfm) as json_file:
    lastfm_data = json.load(json_file)
    
if (debug): print "Success!\n"

if (debug): print "Initialising variables..."

for i in range(len(user_data["f_ids"])):
    user_data["f_ids"][i] = int(user_data["f_ids"][i])
    
friends_ids = Counter(user_data["f_ids"])

active_friends = friends_ids.most_common()

active_fb = {}
indexes = {}
for f_id in active_friends:
    indexes[f_id[0]]=[]

for i in range(len(user_data["f_ids"])):
    if user_data["f_ids"][i] in indexes:
        indexes[user_data["f_ids"][i]].append(i)
        
today = datetime.today()

#difference in days between status update and today
user_data["status_d"] = []

#convert all the dates from facebook and lastfm to a common format and group them
for i in range(len(user_data["status_dates"])):
    date_fb = datetime.strptime(user_data["status_dates"][i], '%Y-%m-%dT%H:%M:%S+0000')
    user_data["status_d"].append((today - date_fb).days)

#difference in days between today and status update
user_data["status_f_d"] = []

#convert all the dates from facebook and lastfm to a common format and group them
for i in range(len(user_data["f_dates"])):
    date_fb = datetime.strptime(user_data["f_dates"][i], '%Y-%m-%dT%H:%M:%S+0000')
    user_data["status_f_d"].append((today - date_fb).days)

#difference in days between today and track play
lastfm_data["recent_d"] = []

for i in range(len(lastfm_data["recent_date"])):
    trackdate = datetime.fromtimestamp(lastfm_data["recent_time"][i])
    lastfm_data["recent_d"].append((today - trackdate).days)
    
#for most active fb user
fb_id = active_friends[1][0]
data_index = indexes[fb_id]
sentiment = [user_data["f_sentiment_clean_en"][i] for i in data_index]
delay = [user_data["status_f_d"][i] for i in data_index]

if (debug): print "Aligning mood and tracks..."

#create the empty holder for the mood and playlist data
mood_month = []
for i in range(30):
    date_mood = today-timedelta(days=i)
    mood_month.append({"mood":0,"tracks":[],"date":date_mood.strftime('%x')})

#cluster the results (sentiment and played songs) according to date (days between today and date of sentiment)
delay_cluster = Counter(delay)
delay_grp = [d[0] for d in delay_cluster.most_common()]
delay_count = [d[1] for d in delay_cluster.most_common()]
delay_dic = dict(zip(delay_grp,delay_count))

for i in range(len(delay)):
    mood_month[delay[i]]["mood"] += sentiment[i]
#    mood_month[delay[i]]["mood"] += sentiment[i]/float(delay_dic[delay[i]])
    
if (debug): print "Filling mood chart..."

#calculate mood and fill month chart
for i in range(len(lastfm_data["recent_d"])):
    if lastfm_data["recent_d"][i] < 30:
        mood_month[lastfm_data["recent_d"][i]]["tracks"].append(lastfm_data["recent_tracks"][i])
        
for mm in mood_month:
    tracks = Counter(mm["tracks"]).most_common()
    trck = [t[0] for t in tracks]
    plyd = [t[1] for t in tracks]
    mm["tracks"] = dict(zip(trck,plyd))
    
if (debug): print "Determining good mood playlist..."

#calculate the mood playlist
happy_playlist = []
for mm in mood_month:    
    if mm["mood"] > 0.1:
        for trck in mm["tracks"]:
            happy_playlist.append(trck) #append once
            if trck in lastfm_data["fav_tracks"]:
                happy_playlist.append(trck) #small boost for fav songs
    if mm["mood"] > 0.5:
        for trck in mm["tracks"]:
            for i in range(mm["tracks"][trck]): #already appended once
                happy_playlist.append(trck) #append according to number of plays
                if trck in lastfm_data["fav_tracks"]:
                    happy_playlist.append(trck) #small boost for fav songs

#get the top x songs
top_x = 20

happy_counter = Counter(happy_playlist).most_common(top_x)    

if len(happy_counter) < top_x:
    k = min(top_x-len(happy_counter),len(lastfm_data["top_tracks"])) #calculate upper boundary
    happy_playlist.extend(lastfm_data["top_tracks"][:k])
    
happy_counter = Counter(happy_playlist).most_common(top_x) 

happy_trck = [t[0] for t in happy_counter]
happy_plyd = [t[1] for t in happy_counter]

happy_playlist = dict(zip(happy_trck,happy_plyd))
      
wrapper = {}
wrapper["mood_calender"] = mood_month
wrapper["playlist"] = happy_playlist
if (debug): print "Complete"

if (debug): print "\nWriting data to file: {0}/Mood_results_{1}.json\n".format(directory, fb_id)
#check if directory exists if not then make it
if not os.path.exists(directory):
    os.makedirs(directory)

with open('{0}/Mood_results_{1}.json'.format(directory,fb_id), 'w') as outfile:
    json.dump(wrapper, outfile, indent = 4)
    
with open('{0}/Mood_results.json'.format(directory,fb_id), 'w') as outfile:
    json.dump(wrapper, outfile, indent = 4)
    
if (debug): print "Finished!" 

