'''
ucitwitter.py
Gokul Pillai
ICS 32A
11/27/2018
'''

import twitter
import geocoder     #geocoder used to determine my own location
import nltk
from nltk.corpus import stopwords   #used to remove stopwords from tweets

g = geocoder.ip('me')
myLoc = g.latlng
myLoc.append("5mi")     #used to make the format proper for the GetSearch method

api = twitter.Api(consumer_key="1GgePT3W46OTcm2gS9ZF6Yxql",
                  consumer_secret="QGMmyKJx0YS92CcCVFHie2Ke9CGFCJWGrGauGgaORBbtu996ZJ",
                  access_token_key="1059975898886107138-tV3IdasjD9JaKCkGbbObmlAA15tUaU",
                  access_token_secret="vaUUsieYEReMXLDrgnzz56ENQPoIIVVkRvl27A5J75QlJ")

def filterTimeline(keyword):    #goes through the home timeline and prints out tweets that don't have the keyword
    status = api.GetHomeTimeline()
    for x in status:
        if(not(keyword in x.text)):
            print(x.text)

def commonWord(username):   #finds the most common word of the last 2000 tweets of a user
    status = api.GetUserTimeline(screen_name = username, count = 2000)
    tempList = []
    for x in status:    #adds each individual word from the last 2000 tweets to a list
        tempList.extend(x.text.split())

    counter = 0
    while(counter < len(tempList)):
        x = tempList[counter]
        for y in x:
            if(not(y.isdigit() or y.isalpha())):    #getting rid of extraneous punctuation
                tempList[counter] = x[0:x.index(y)] + x[x.index(y)+1:]
        counter+=1

    wordList = []   #holds each unique word from the tweets
    wordCountList = []  #holds how many times the corresponding word(matched by index) shows up in the tweets
    for x in tempList:
        if(not(x in wordList) and x != "RT" and not x.lower() in stopwords.words('english')):    #adds words that haven't already been added and aren't uninteresting to a new list
            wordList.append(x)
            wordCountList.append(countWord(x, tempList))    #calls the countWord method to determine how many times the word shows up in the tweets

    print(wordList[wordCountList.index(max(wordCountList))])    #prints out the most common word

def countWord(word, tList):     #determines how many times the word shows up in the tweets
    count = 0
    for x in tList:
        if x == word:
            count+=1
    return count

def searchArea(keyword = None, location = myLoc):   #prints out all the tweets within a week within a 5 mile radius that contain the keyword
    objList = []    #holds the each tweet
    if(isinstance(location, list)):     #used for if the location geocode is a list
        while(location[2] != "0mi"):    #iterates from 5 miles all the way down to 1
            numMi = int(location[2][0])
            objList.extend(printGetSearch(keyword, location))
            location.pop()
            location.append(str(numMi - 1) + "mi")
    elif(isinstance(location, str)):    #used for if the location geocode is a string
        numMi = int(location[-3])
        while(numMi != 0):              #iterates from 5 miles all the way down to 1
            objList.extend(printGetSearch(keyword, location))
            numMi -= 1
            location = location[0:-3] + str(numMi) + location[-2:]
    objNewList = []
    for x in objList:
        if(not x in objNewList):    #used to make sure that there aren't any duplicates of tweets, and then prints it out
            objNewList.append(x)
            print(x.text)


def printGetSearch(keyword, location):      #returns a list with all the tweets based on the specified radius
    from datetime import datetime, timedelta    #uses datetime to determine the current date to find the date from a week ago
    now = datetime.now()
    weekAgo = str(now - timedelta(days=7))
    weekAgo = weekAgo[0:10]

    status = api.GetSearch(term = keyword, since = weekAgo, geocode=location, count = 200)     #method to find all the tweets with keyword within radius since a week ago
    objList = []
    for x in status:
        objList.append(x)   #adds all the tweets to a list
    return objList

keyW1 = input("Please enter a keyword: ")
print("")
filterTimeline(keyW1)
print("")

userN = input("Please enter a username: ")
print("")
commonWord(userN)
print("")

keyW2 = input("Please enter a keyword: ")
print("")
loc = input("Please enter a location in geocode format: ")
print("")
if(len(loc) == 0):
    searchArea(keyW2)
else:
    searchArea(keyW2, loc)
