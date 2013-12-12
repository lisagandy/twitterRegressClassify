import MySQLdb as mdb
import csv
import utilities as util

class RetweetCollector:
   
   conn = None
   close = None
   #num_users = 0
   outFolder = '/home/lisagandy/retweet_stats/'

   def __init__(self,targetWord="",outDir="",threads=False):
       #if RetweetCollector.num_users==0:
           #RetweetCollector.num_users = util.lenCelebIDS()
           self.conn = mdb.connect('localhost', 'lisagandy', 'Chicago!!', 'TwitterCollector');
           self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
   
   def getRetweetsCeleb(self,user_id):
      fOut,fileExists = self.getFileHandleWrite(user_id)
      if fileExists:
         return
      sqlStr = 'Select tweet_id from tweets where user_id=%s' % user_id
      print user_id
      print "----------"
      self.cursor.execute(sqlStr)
      resAll = self.cursor.fetchall()
      lsFollowers = []
      for res in resAll:
         sqlStr2 = "Select sum(retweet_count) from tweets where original_tweet_id=%s;" % (res['tweet_id'])
         #print sqlStr2
         self.cursor.execute(sqlStr2)
         resAll2 = self.cursor.fetchone()
         if resAll2 and len(resAll2) > 0 and resAll2.values()[0]!=None:
            lsFollowers.append([resAll2.values()[0],res['tweet_id']])
      
      if len(lsFollowers) > 0:
         print lsFollowers
      else:
         return   
      self.createOrGetCSV(user_id,lsFollowers,fOut)   
     
   def getFileHandleWrite(self,user_id):
         fileExists=True
         fOut = None
         try:
            with open('%s/%s.csv' % (self.outFolder,user_id),'r') as fOut: pass
         except IOError as e:
            fileExists=False
            fOut = open('%s/%s.csv' % (self.outFolder,user_id),'w')

         return fOut,fileExists

   def createOrGetCSV(self,user_id,tweets,fOut):
         

         fields = ['user_id','tweet_id','retweet_count']
         fDictWriter = csv.DictWriter(fOut,fields)
         fOut.write(','.join(fields)+'\n') #write header if not already there

         for info in tweets:
            # if dTweet['original_tweet_id']==0:
            dTemp={}
            dTemp['user_id'] = user_id
            dTemp['tweet_id'] = info[1]
            dTemp['retweet_count'] = info[0]
            fDictWriter.writerow(dTemp)
         fOut.close()      
  
   def celebIDS(self):
      for i,user_id in enumerate(util.getCelebIDS()):
         print i
         self.getRetweetsCeleb(user_id)
      
   def __del__(self):
      self.conn.close()
      
if __name__ == '__main__':
   rc = RetweetCollector()
   rc.celebIDS()
         #rc.getNumUsers()