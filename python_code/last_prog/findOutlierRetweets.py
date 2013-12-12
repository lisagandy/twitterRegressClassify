import os
import csv
import utilities as util
import MySQLdb as mdb

class RetweetOutlierFinder:
   inFolder = '/home/lisagandy/retweet_stats/'
   outCSV = '/home/lisagandy/outlier_tweets_new_neg_pos.csv'
   
   lsAllIDS = []
   lsTweets=[]
   fDictWriter = None
   fOut = None
   
   def __init__(self):
      self.fOut = open(self.outCSV,'w')
      fields = ['user_id','user_name','tweet_id','tweet_text','retweet_count','positive_words','negative_words']
      self.fOut.write(','.join(fields) + '\n')
      self.fDictWriter = csv.DictWriter(self.fOut,fields) 
      self.conn = mdb.connect('localhost', 'lisagandy', 'Chicago!!', 'TwitterCollector');
      self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
   
   
   def getOriginalTweeterInfo(self,tweet_id):
      sqlStr = "Select user_id from tweets where tweet_id=%s" % tweet_id
      #print sqlStr
      user_id=None
      self.cursor.execute(sqlStr)   
      ret = self.cursor.fetchone()
      if ret:
          user_id = ret['user_id']
      
      user_name=None
      if user_id:
         user_name = self.getUserName(user_id)
      
      return (user_name,user_id)

   def getUserName(self,user_id):
       sqlStr = 'Select name from user_info where user_id=%s' % user_id
       self.cursor.execute(sqlStr)   
       ret = self.cursor.fetchone()
       if ret:
          return ret['name']
       else:
          return None
   
   def getTweetText(self,tweet_id):
      sqlStr = 'Select tweet_text from tweets where tweet_id=%s' % tweet_id
      self.cursor.execute(sqlStr)   
      ret = self.cursor.fetchone()
      if ret:
          tweet_text = ret['tweet_text']
          tweet_text = tweet_text.replace("\n","")
          tweet_text = tweet_text.replace("\r","")
          tweet_text = tweet_text.replace("^","")
          #return ret['tweet_text']
          return tweet_text
      else:
          return None
   
   def getTweetTime(self,tweet_id):
      sqlStr = 'Select created_at from tweets where tweet_id=%s' % tweet_id
      self.cursor.execute(sqlStr)   
      ret = self.cursor.fetchone()
      if ret:
         return ret['created_at']
      else:
         return None
   
   def findOutlierRetweets(self,fileName):
      fDictReader = csv.DictReader(open(fileName,'rU'))
      #user_id,tweet_id,retweet_count,retweet_ids
      lsRows = [row for row in fDictReader]
      lsNums = [int(row['retweet_count']) for row in lsRows if row['retweet_count']!=""]
      if len(lsNums) == 0:
         return
      print lsNums   
      for row in lsRows:
         if row['retweet_count'] == '':
            continue
            
         if row['tweet_id'] in self.lsAllIDS:
            continue
         self.lsAllIDS.append(row['tweet_id'])
         #print int(row['retweet_count'])
         #print lsNums
         boolOut = util.isOutlier(int(row['retweet_count']),lsNums)
         #print boolOut
         if boolOut==True and int(row['retweet_count']) > 10:
            self.writeOutlierTweet(row)
         #else:
            #print ""
         
   def writeOutlierTweet(self,row):  
      
      dOut = {}
      dOut['user_id'] = row['user_id']
      dOut['tweet_id'] = row['tweet_id']
      dOut['retweet_count'] = int(row['retweet_count'])
      dOut['user_name'] = self.getUserName(row['user_id'])
      dOut['tweet_text'] = self.getTweetText(row['tweet_id'])
      if dOut['tweet_text'] in self.lsTweets or util.tweetIncomp(dOut['tweet_text']):
            return
      self.lsTweets.append(dOut['tweet_text'])
      
      #print dOut
      #print ""
      pos_words = util.getPosWords(dOut['tweet_text'])
      dOut['positive_words']="NONE"
      if len(pos_words)>0:
          dOut['positive_words'] = "&".join(pos_words)
      
      neg_words = util.getNegWords(dOut['tweet_text'])
      dOut['negative_words']="NONE"
      if len(neg_words)>0: 
              dOut['negative_words'] = "&".join(neg_words)
      self.fDictWriter.writerow(dOut)

      
      
   def openFiles(self):
      lsFileNames = os.listdir(self.inFolder)
      for i,fileName in enumerate(lsFileNames):
         print i
         #print self.inFolder + fileName
         self.findOutlierRetweets(self.inFolder + fileName)
         # if i==1000:
         #             assert 0
      self.fOut.close()
      
      
if __name__ == '__main__':
   fo = RetweetOutlierFinder()
   fo.openFiles()      