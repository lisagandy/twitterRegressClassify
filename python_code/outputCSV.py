import MySQLdb as mdb
import csv
import time
class OutputCSV:
    
    conn=None
    cursor=None
    dMedia=None


    def __init__(self):
        self.conn = mdb.connect('localhost', 'lisagandy', 'Chicago!!', 'TwitterCelebs');
        self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
        self.dMedia=None

    def getLocalOutliers(self):
        sqlStr = "Select tweet_id from local_outlier;"
        self.cursor.execute(sqlStr)
        resAll=[]
        res = self.cursor.fetchone()
        
        while res!=None:
            resAll.append(res)
            res = self.cursor.fetchone()

        resAll = [res['tweet_id'] for res in resAll]
        return resAll
        
    def getTweetQuestion(self)  :
        sqlStr="Select tweet_id from tweet_question;"
        self.cursor.execute(sqlStr)
        resAll = self.cursor.fetchall()

        resAll = [res['tweet_id'] for res in resAll]
        return resAll

    def getTweetMentions(self)  :
        sqlStr="Select distinct tweet_id from mentions;"
        self.cursor.execute(sqlStr)
        resAll = self.cursor.fetchall()

        resAll = [res['tweet_id'] for res in resAll]
        return resAll   


    def getHashTags(self):
        sqlStr = "Select distinct tweet_id from hashtags;"
        self.cursor.execute(sqlStr)
        resAll=[]
        res = self.cursor.fetchone()

        while res!=None:
            resAll.append(res)
            res = self.cursor.fetchone()

        resAll = [res['tweet_id'] for res in resAll]
        return resAll

    def getURLS(self):
       
        sqlStr = "Select tweet_id,type_media from urls;"
        self.cursor.execute(sqlStr)
        resAll=[]
        res = self.cursor.fetchone()

        while res!=None:
            resAll.append(res)
            res = self.cursor.fetchone()
    
        self.dMedia={}
        for res in resAll:
            self.dMedia[res['tweet_id']] = res['type_media']

    def getTypeMedia(self,tweet_id):
        if tweet_id not in self.dMedia:
            return False,False,False
        typeMedia = self.dMedia[tweet_id]
        hasPhoto=False
        hasVideo=False
        if typeMedia=="photo":
            hasPhoto=True
        elif typeMedia=="video":
            hasVideo=True
        return True,hasPhoto,hasVideo

    def getUserIDS(self):
        sqlStr = "Select tweet_id,user_id from tweets where tweet_id in (Select tweet_id from local_outlier);" 
        self.cursor.execute(sqlStr)
        resAll = self.cursor.fetchall()
        dRet={}
        for dRes in resAll:
            dRet[dRes['tweet_id']] = dRes['user_id']
        return dRet

    def getNumFollowers(self):
        sqlStr = "Select followers,user_id from user_info where user_id in (Select user_id from tweets where tweet_id in (Select tweet_id from local_outlier))";

        self.cursor.execute(sqlStr)
        resAll = self.cursor.fetchall()
        dRet={}
        for dRes in resAll:
            dRet[dRes['user_id']] = dRes['followers']
        return dRet
            
    def writeCSV(self):
        fields=['tweet_id','user_id','num_followers','has_mentions','is_question','has_url','has_hashtag','has_video','has_photo','is_outlier']
        f = open("/home/lisagandy/tweets_out_with_user_info.csv",'w')
        f.write(','.join(fields)+'\n')
        fDictWriter = csv.DictWriter(f,fields)

        lsTweetQuestion = self.getTweetQuestion()
        lsTweetQuestion.sort()
        
        startTime = time.time()
        lsMentions = self.getTweetMentions()
        lsMentions.sort()
        elapsedTime = time.time()-startTime
        print "ELAPSED TIME IS " + str(elapsedTime)
        
        lsHashTag = self.getHashTags()
        lsHashTag.sort()

        self.getURLS()

        startTime = time.time()
        dUsers = self.getUserIDS()
        elapsedTime = time.time()-startTime
        print "ELAPSED TIME IS " + str(elapsedTime)
        
        startTime = time.time()
        dNumFollowers = self.getNumFollowers()
        elapsedTime = time.time()-startTime
        print "ELAPSED TIME IS " + str(elapsedTime)

        for i in range(1,726000,5000):
            #startTime = time.time()
            #if i > 1:
                #assert 0
            print "*****************************************"
            sqlStr = "Select tweet_id from local_outlier limit %d,5000;" % (i)
            print sqlStr
            self.cursor.execute(sqlStr)
            resAll=[]
            resAll = self.cursor.fetchall()
            print "LENGTH OF RESULT"
            print len(resAll)
            for j,res in enumerate(resAll):
                    #print j
                    d={}
                    tweet_id=res['tweet_id']
  
                    d['tweet_id'] = tweet_id
                    
                    if tweet_id in lsMentions:
                         d['has_mentions']=True
                    else:
                         d['has_mentions']=False 

                    if tweet_id in lsTweetQuestion:
                        d['is_question'] = True
                    else:
                        d['is_question'] = False
            
                    if tweet_id in lsHashTag:
                        d['has_hashtag'] = True
                    else:
                        d['has_hashtag'] = False
            
                    d['is_outlier']=True

                    d['has_url'],d['has_photo'],d['has_video'] = self.getTypeMedia(tweet_id)
                    d['user_id'] = dUsers[tweet_id]

                    d['num_followers'] = dNumFollowers[d['user_id']]
                    fDictWriter.writerow(d)
            #elapsedTime = time.time()-startTime
            #print "ELAPSED TIME IS " + str(elapsedTime)
        f.close()   
            

if __name__ == '__main__':
    
        oc = OutputCSV()
        oc.writeCSV()
        
    