import MySQLdb as mdb
import numpy as np
import csv

class FindTweetOutliers:
    
    conn = None
    cursor = None
    upperRange = None   
        
    def __init__(self):
        self.conn = mdb.connect('localhost', 'lisagandy', 'Chicago!!', 'TwitterCelebs');
        self.cursor = self.conn.cursor(mdb.cursors.SSCursor)
    
    def getValidUsers(self):
        sqlStr = "Select user_id from user_info where real_account=1 and top5000=1;"
        self.cursor.execute(sqlStr)
        dRes = self.cursor.fetchall()
        dRes = [d[0] for d in dRes]
        return dRes
    
    #uses the MADe detection method for finding outliers
    def isOutlier(self,num,lsAllNums,newNum=True):

       if newNum:
          origMed = np.median(lsAllNums)
          lsRangeMed = [abs(num2-origMed) for num2 in lsAllNums]
          MADe = np.median(lsRangeMed) * 1.483 * 2
          self.upperRange = origMed + MADe

       if num >= self.upperRange:
          return True
       else:
          return False
    
    def updateUserOutlier(self,tweet_id):
        sqlStr = "Insert into local_outlier(tweet_id) values (%s)" % tweet_id
        try:
            self.cursor.execute(sqlStr)
            self.conn.commit()
        except Exception,ex:
             pass
    
    def updateGlobalOutlier(self,tweet_id):
        sqlStr = "Insert into global_outlier(tweet_id) values (%s)" % tweet_id
        try:
            self.cursor.execute(sqlStr)
            self.conn.commit()
        except Exception,ex:
             pass

    def markUserOutliers(self,user_id):
        sqlStr = "Select retweet_count,tweet_id from tweets where user_id=%s and retweet_count>0;" % user_id    
        print sqlStr
        self.cursor.execute(sqlStr)
        dRes = self.cursor.fetchall()
        lsNumRetweets = [d[0] for d in dRes]
        if len(lsNumRetweets) == 0:
            print "PROBLEM IN NUM RETWEETS"
            #assert 0
            
        for i,d in enumerate(dRes):
            boolOutlier=None
            if i==1:
                boolOutlier = self.isOutlier(d[0],lsNumRetweets,True)
            else:
                boolOutlier = self.isOutlier(d[0],lsNumRetweets,False)
            
            if boolOutlier:
                #print 'MARKING AS OUTLIER'
                self.updateUserOutlier(d[1])
            #else:
                #print 'NOT MARKING AS OUTLIER'
                
    def findLocalOutliers(self):
        lsUserIDS = self.getValidUsers()
        print len(lsUserIDS)
        for i,user_id in enumerate(lsUserIDS):
            print i
            print "__________________________"
            if i<267:
                continue
            self.markUserOutliers(user_id)
    
    


    def printAllTweets(self):
        fOut = open("all_tweets.csv",'w')
        fields = ['num_retweets']
        fDictWriter = csv.DictWriter(fOut,fields)
        fOut.write(','.join(fields)+'\n')
        
        lsUserIDS = self.getValidUsers()
        #print len(lsUserIDS)
        for i,user_id in enumerate(lsUserIDS):
            print i
            print "______________"
            sqlStr = "Select retweet_count from tweets where user_id=%s and retweet_count>0;" % user_id 
            #print sqlStr
            self.cursor.execute(sqlStr)
            dRes = self.cursor.fetchall()
            for d in dRes:
                dOut={}
                dOut['num_retweets'] = d[0]
                fDictWriter.writerow(dOut)
            
        fOut.close()


    def findGlobalOutliers(self):
            sqlStr = "Select tweet_id from tweets where retweet_count>21"
            self.cursor.execute(sqlStr)
            dRes = self.cursor.fetchall()
            print len(dRes)
            for i,d in enumerate(dRes):
                print i
                self.updateGlobalOutlier(d[0])
                
if __name__ == '__main__':
    ft = FindTweetOutliers()
    #ft.findLocalOutliers()
    ft.findGlobalOutliers()
