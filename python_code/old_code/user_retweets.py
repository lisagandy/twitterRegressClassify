import MySQLdb as mdb
import csv

class RetweetCollector:

   conn = None
   close = None
   num_users = 0
   outFolder = '/home/lisagandy/retweet_stats/'

   def __init__(self,targetWord="",outDir="",threads=False):
       self.conn = mdb.connect('localhost', 'lisagandy', 'Chicago!!', 'TwitterCollector');
       self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
       if RetweetCollector.num_users==0:
          RetweetCollector.num_users = self.getNumUsers()
          #print RetweetCollector.num_users
   
   def __del__(self):
      self.conn.close()
   
   def getUsers(self,start=0,limit=10):
      sqlStr = 'Select user_id from users limit %d,%d;' % (start,limit)
      #print sqlStr
      self.cursor.execute(sqlStr)   
      return self.cursor.fetchall()
   
   def getNumUsers(self):
       sqlStr = 'Select Count(*) from users;'
       self.cursor.execute(sqlStr)
       res = self.cursor.fetchone()
       return res.values()[0]
   
   # def getFileHandleAbs(self,user_id):
   #       fOut = open('%s/%s.csv' % (self.outFolder,user_id),'w')
   #       return fOut
      
   def getFileHandleWrite(self,user_id):
      fileExists=True
      fOut = None
      try:
         with open('%s/%s.csv' % (self.outFolder,user_id),'r') as fOut: pass
      except IOError as e:
         fileExists=False
         fOut = open('%s/%s.csv' % (self.outFolder,user_id),'w')
         
      return fOut,fileExists
            
   def createOrGetCSV(self,user_id,tweets):
      fOut,fileExists = self.getFileHandleWrite(user_id)
      if fileExists:
         return
      
      fields = ['user_id','tweet_id','retweet_count','retweet_ids','original_tweet_id']
      fDictWriter = csv.DictWriter(fOut,fields)
      fOut.write(','.join(fields)+'\n') #write header if not already there
         
      for dTweet in tweets:
         # if dTweet['original_tweet_id']==0:
         dTemp={}
         dTemp['user_id'] = user_id
         dTemp['tweet_id'] = dTweet['tweet_id']
         dTemp['retweet_count'] = dTweet['retweet_count']
         dTemp['original_tweet_id'] = dTweet['original_tweet_id']
         fDictWriter.writerow(dTemp)
         #             fOut.write(dTemp)
         #          else:
         #self.updateCSV(dTweet['original_tweet_id'],dTweet['retweet_count'])
      
      fOut.close()
   
   def getUserTweets(self,user_id):
       sqlStr = 'Select tweet_id,retweet_count,original_tweet_id from tweets where user_id=%s' % user_id
       self.cursor.execute(sqlStr)
       res = self.cursor.fetchall()
       if len(res) < 10:
          #print len(res)
          #print 'TOO FEW TWEETS'
          return None
       else:
          return res
       return res
       
   def get_user_retweet_stats(self):
      print self.num_users
      for i in range(0,self.num_users,10):
         #print i
         resUsers = self.getUsers(start=i,limit=10)
         #print len(resUsers)
         for dRes in resUsers:
            tweets= self.getUserTweets(dRes['user_id'])
            if tweets:
               self.createOrGetCSV(dRes['user_id'],tweets)
     
if __name__ == '__main__':
   rc = RetweetCollector()
   rc.get_user_retweet_stats()
   #rc.getNumUsers()  