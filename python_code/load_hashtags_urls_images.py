import MySQLdb as mdb
import os
import simplejson
import datetime
import calendar
import csv
from django.utils.encoding import smart_str, smart_unicode

class LoadExtra:
    
    realUsers = []
    celeb_directory="/home/lisagandy/celebs/"
    conn = None
    cursor = None
        
    def __init__(self):
        self.conn = mdb.connect('localhost', 'lisagandy', 'Chicago!!', 'TwitterCelebs');
        self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
        print "getting real users"
        self.getRealUsers()
     
    def getRealUsers(self):
         sqlStr = "Select user_id from user_info where real_account=1 and top5000=1";
         self.cursor.execute(sqlStr);
         self.realUsers = [d['user_id'] for d in self.cursor.fetchall()]
         

    def loadHashTags(self,tweet_id,lsHashTag):
        for tag in lsHashTag[0:1]:
            try:
                sqlStr = "Insert into hashtags (tweet_id,hashtag) values ('%s','%s')" % (tweet_id,tag['text'])
                #print sqlStr
                self.cursor.execute(sqlStr)
                self.conn.commit()
            except Exception,ex:
                if str(ex).find('Duplicate')==-1:
                    print ex
                #print str(ex)
                #if str(ex).find('Expect') > -1:
                    #assert 0
                #print ex


    def loadURLS(self,tweet_id,lsURLS):
        for url in lsURLS:
            try:
                sqlStr = "Insert into urls (tweet_id,url) values ('%s','%s')" % (tweet_id,url['expanded_url'])
                #print sqlStr
                self.cursor.execute(sqlStr)
                self.conn.commit()
            except Exception,ex:
                #print ex
                if str(ex).find('Duplicate')==-1:
                        print ex

    
    def loadMedia(self,tweet_id,lsURLS):
        for url in lsURLS[0:1]:
            try:
                sqlStr = "Insert into media (tweet_id,media_url,type) values ('%s','%s','%s')" % (tweet_id,url['expanded_url'],url['type'])
                #print sqlStr
                self.cursor.execute(sqlStr)
                self.conn.commit()
            except Exception,ex:
                if str(ex).find('Duplicate')==-1:
                        print ex
                
    def loadMentions(self,tweet_id,lsMentions):
        #print lsMentions

        for mention in lsMentions[0:1]:
            try:
                sqlStr = "Insert into mentions (tweet_id,mention) values ('%s','%s')" % (tweet_id,mention['screen_name'])
                #print sqlStr
                self.cursor.execute(sqlStr)
                self.conn.commit()
            except Exception,ex:
                if str(ex).find('Duplicate')==-1:
                        print ex
                        

    def loadTweet(self,dTweet):
        
        
        lsMentions = dTweet['entities']['user_mentions']
        lsHashTag = dTweet['entities']['hashtags']
        lsURLS =  dTweet['entities']['urls']
        lsMedia=[]
        if 'media' in dTweet['entities'].keys():
            lsMedia = dTweet['entities']['media']
           
        tweetID = dTweet['id']
        
        #if not self.isOutlierDB(tweetID):
            #return
        #assert 0
        self.loadHashTags(tweetID,lsHashTag)
        self.loadMedia(tweetID,lsMedia)
        self.loadURLS(tweetID,lsURLS)
        self.loadMentions(tweetID,lsMentions)
        
    def loadJSON(self,strD):
        lsStrD = strD.split("\n")
        strDFirst = simplejson.loads(lsStrD[0])
        #is the user a "real" celeb
        if strDFirst['user']['id'] not in self.realUsers:
            print 'not a real user'
            return
            
        #print len(lsStrD)
        i=1
        for strD in lsStrD:
            #print i
            #i+=1
            try:
                dTweet = simplejson.loads(strD)
            except Exception,ex:
                print ex
                print strD
                print ""
                continue
            
            #print dTweet
            #print dTweet.keys()    
            self.loadTweet(dTweet)
            
      
    def openAllFiles(self):

        lsFileNames = os.listdir(self.celeb_directory);
        #print lsFileNames
        print len(lsFileNames)
        start=False
        for i,fileName in enumerate(lsFileNames):
            print i
            print fileName
            print "*****************"
            if i<2011:
                continue
            if fileName==".DS_Store":
                continue
                
            #strJSON = open(self.celeb_directory+fileName).read()
            strFile = self.celeb_directory+fileName
            print strFile
            strD = open(strFile).read()
            self.loadJSON(strD)


if __name__ == '__main__':
    ld = LoadExtra()
    ld.openAllFiles();
