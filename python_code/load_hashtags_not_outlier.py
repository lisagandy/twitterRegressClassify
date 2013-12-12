import MySQLdb as mdb
import os
import simplejson
import datetime
import calendar
import csv
from django.utils.encoding import smart_str, smart_unicode

class LoadExtra:
    
    celeb_directory="/home/lisagandy/celebs/"
    conn = None
    cursor = None
        
    def __init__(self):
        self.conn = mdb.connect('localhost', 'lisagandy', 'Chicago!!', 'TwitterCelebs');
        self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
        
    def isNotOutlierDB(self,tweetID):
        sqlStr = "Select * from sample where tweet_id=%s" % tweetID
        #print sqlStr
        self.cursor.execute(sqlStr)
        lsRes = self.cursor.fetchone()
        if lsRes==None:
            return False
        return True

    def loadHashTags(self,tweet_id,lsHashTag):
        for tag in lsHashTag:
            try:
                sqlStr = "Insert into hashtags_noto (tweet_id,hashtag) values ('%s','%s')" % (tweet_id,tag['text'])
                #print sqlStr
                self.cursor.execute(sqlStr)
                self.conn.commit()
            except Exception,ex:
                #print str(ex)
                if str(ex).find('Expect') > -1:
                    assert 0
                #print ex


    def loadURLS(self,tweet_id,lsURLS):
        for url in lsURLS:
            try:
                sqlStr = "Insert into urls_noto (tweet_id,url) values ('%s','%s')" % (tweet_id,url['expanded_url'])
                #print sqlStr
                self.cursor.execute(sqlStr)
                self.conn.commit()
            except Exception,ex:
                #print ex
                if str(ex).find('Expect') > -1:
                    assert 0

    
    def loadMedia(self,tweet_id,lsURLS):
        for url in lsURLS:
            try:
                sqlStr = "Insert into media_noto (tweet_id,media_url,type) values ('%s','%s','%s')" % (tweet_id,url['expanded_url'],url['type'])
                #print sqlStr
                self.cursor.execute(sqlStr)
                self.conn.commit()
            except Exception,ex:
				print ex
                
    def loadMentions(self,tweet_id,lsMentions):
        #print lsMentions

        for mention in lsMentions:
            try:
                sqlStr = "Insert into mentions_noto (tweet_id,mention) values ('%s','%s')" % (tweet_id,mention['screen_name'])
                #print sqlStr
                self.cursor.execute(sqlStr)
                self.conn.commit()
            except Exception,ex:
                print ex
                #pass
                #print ex
                        
                        

    def loadTweet(self,dTweet):
        #lsMentions = dTweet['entities']['user_mentions']
        lsHashTag = dTweet['entities']['hashtags']
        lsURLS =  dTweet['entities']['urls']
        #lsMedia=[]
        #if 'media' in dTweet['entities'].keys():
        	#lsMedia = dTweet['entities']['media']
           
        tweetID = dTweet['id']
        
        if not self.isNotOutlierDB(tweetID):
            return
        #assert 0
        self.loadHashTags(tweetID,lsHashTag)
        #self.loadMedia(tweetID,lsMedia)
        self.loadURLS(tweetID,lsURLS)
        #self.loadMentions(tweetID,lsMentions)
        
    def loadJSON(self,strD):
        lsStrD = strD.split("\n")
        #bFirst=True
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