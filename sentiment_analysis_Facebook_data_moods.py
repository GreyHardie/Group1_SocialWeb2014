# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 22:24:22 2014

@author: Group 1 - Social Web 2014
"""
#import regex
import re
import os,json
from textblob import TextBlob

#verbose mode
debug = True

#directions to where the data file is stored
directory = "collected_data/"
user_file = "facebook_data.json"

if (debug): print "Loading user facebook data from JSON file"

with open(directory+user_file) as json_file:
    user_data = json.load(json_file)

if (debug): print "Success!\n"

#preprocess the texts that will undergo sentiment analysis
def cleanText(dirty_text):
    #Convert to lower case
    cleaner_text = dirty_text.lower()
    #Convert www.* or https?://* to URL
    cleaner_text = re.sub('((www\.[\s]+)|(https?://[^\s]+))','URL',cleaner_text)
    #Convert @username to AT_USER
    cleaner_text = re.sub('@[^\s]+','AT_USER',cleaner_text)
    #Remove additional white spaces
    cleaner_text = re.sub('[\s]+', ' ', cleaner_text)
    #Replace #word with word
    cleaner_text = re.sub(r'#([^\s]+)', r'\1', cleaner_text)
    #trim
    clean_text = cleaner_text.strip('\'"')
    return clean_text
    
#look for 2 or more repetitions of character and replace with the character itself
def removeRepeat(s):
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')
 
    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
    
#initialize english stopWords
stopWords = []
stopWords = getStopWordList('stopwords.txt')

#start get feature Vector only important words
def getFeatureVector(text):
    featureVector = []
    #split text into words
    words = text.split()
    for w in words:
        #replace two or more with two occurrences
        w = removeRepeat(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
    
if (debug): print "Translating to english text..."

#Detect language if no english translate to english using goolge api
user_data["status_en"] = []
for status in user_data["statuses"]:
    blob = TextBlob(status)
    if blob.detect_language()!='en':
        blob = blob.translate(to='en')
    user_data["status_en"].append(" ".join(blob.raw_sentences))

user_data["f_status_en"] = []
for status in user_data["f_statuses"]:
    blob = TextBlob(status)
    if blob.detect_language()!='en':
        blob = blob.translate(to='en')
    user_data["f_status_en"].append(" ".join(blob.raw_sentences))

if (debug): print "Cleaning text..."

#clean the text to remove to remove any rubbish characters
user_data["clean_status_en"] = []
for status in user_data["status_en"]:
    clean = cleanText(status)
    user_data["clean_status_en"].append(clean)
 
user_data["clean_f_status_en"] = []
for status in user_data["f_status_en"]:
    clean = cleanText(status)
    user_data["clean_f_status_en"].append(clean)

#if (debug): print "Removing stopwords..."  

#remove stopwords leaving a feature vector of important words
#this did not give good results in the sentiment analysis as we stripped away the emoticons and smileys we therefore removed this from the next sections

#user_data["clean_status_en_feature"] = []
#for status in user_data["clean_status_en"]:
#    clean = getFeatureVector(status)
#    user_data["clean_status_en_feature"].append(" ".join(clean))
#
#user_data["clean_f_status_en_feature"] = []
#for status in user_data["clean_f_status_en"]:
#    clean = getFeatureVector(status)
#    user_data["clean_f_status_en_feature"].append(" ".join(clean))
    
if (debug): print "Determining sentiment..."

#get sentiment

##cleaned feature vector
#user_data["sentiment_clean_en_feat"] = []
#for status in user_data["clean_status_en_feature"]:
#    blob = TextBlob(status).polarity
#    user_data["sentiment_clean_en_feat"].append(blob)
#
#
#user_data["f_sentiment_clean_en_feat"] = []
#for status in user_data["clean_f_status_en_feature"]:
#    blob = TextBlob(status).polarity
#    user_data["f_sentiment_clean_en_feat"].append(blob)

#cleaned text with stopwords intact
user_data["sentiment_clean_en"] = []
for status in user_data["clean_status_en"]:
    blob = TextBlob(status).polarity
    user_data["sentiment_clean_en"].append(blob)
    
user_data["f_sentiment_clean_en"] = []
for status in user_data["clean_f_status_en"]:
    blob = TextBlob(status).polarity
    user_data["f_sentiment_clean_en"].append(blob)
      
    
if (debug): print "Writing data to file: "+'{0}/sentiment_data.json'.format(directory)

#check if directory exists if not then make it
if not os.path.exists(directory):
    os.makedirs(directory)

with open('{0}/sentiment_data.json'.format(directory), 'w') as outfile:
    json.dump(user_data, outfile, indent = 4)
    
if (debug): print "Finished!" 

