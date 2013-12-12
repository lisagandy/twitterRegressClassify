import MySQLdb as mdb
import os
import simplejson
import datetime
import calendar
import csv
from django.utils.encoding import smart_str, smart_unicode

class LoadDB:
	
	dCal = dict((v,k) for k,v in enumerate(calendar.month_abbr)) 
	celeb_directory="/home/lisagandy/celebs/"
	conn = None
	cursor = None
		
	def __init__(self):
		self.conn = mdb.connect('localhost', 'lisagandy', 'Chicago!!', 'TwitterCelebs');
		self.cursor = self.conn.cursor(mdb.cursors.DictCursor)
		
	
	def userIDExists(self,user_id):
		sqlStr = "Select user_id from user_info where user_id=%s" % user_id;
		self.cursor.execute(sqlStr)
		dRes = self.cursor.fetchone()
		if dRes==None:
			return False
		return True

	def tweetIDExists(self,tweet_id):
		sqlStr = "Select tweet_id from tweets where tweet_id=%s" % tweet_id;
		self.cursor.execute(sqlStr)
		dRes = self.cursor.fetchone()
		if dRes==None:
			return False
		return True

	def getAllTweetIDS(self):
		lsAll=[]
		for i in range(0,7748758,1000000):
			print i
			sqlStr = "Select tweet_id,user_id from tweets limit %d,%d" % (i+1,i+1000000)
			print sqlStr
			
			self.cursor.execute(sqlStr)
			dRes = self.cursor.fetchall()
			lsAll.extend(dRes)
			
		print "LOADED ALL TWEETS"
		return lsAll
		
	def getNumFollowers(self,user_id):
		sqlStr = "Select followers from user_info where user_id=%s;" % user_id
		self.cursor.execute(sqlStr)
		dRes = self.cursor.fetchone()
		return dRes
	
	def getNumRetweets(self,tweet_id):
		sqlStr = "Select retweet_count from tweets where tweet_id=%s;" % tweet_id
		self.cursor.execute(sqlStr)
		dRes = self.cursor.fetchone()
		return dRes
		
	def loadTweet(self,dTweet):
		if self.tweetIDExists(dTweet["id"]):
			return
		lsDate = dTweet["created_at"].split()
		lsTime = lsDate[3].split(":")
		dateObj = datetime.datetime(int(lsDate[-1]),self.dCal[lsDate[1]],int(lsDate[2]),int(lsTime[0]),int(lsTime[1]),int(lsTime[2]))
		strOrigTweetID = "NULL"
		if "retweeted_status" in dTweet.keys():
			strOrigTweetID = dTweet["retweeted_status"]["id"]
			
		strTweetURL = "http://twitter.com/"+dTweet["user"]["id_str"]+"/status/"+dTweet["id_str"]
		strNewText = self.conn.escape_string(smart_str(dTweet["text"]))
		sqlStr = "Insert into tweets(tweet_id,tweet_text,created_at,user_id,retweet_count,original_tweet_id,tweet_url) values (%d,\"%s\",'%s',%d,%d,%s,'%s')";
		sqlStr = sqlStr % (dTweet["id"],strNewText,dateObj.strftime('%Y-%m-%d %H:%M:%S'),dTweet["user"]["id"],int(dTweet["retweet_count"]),strOrigTweetID,strTweetURL);
		try:
			self.cursor.execute(sqlStr)
			self.conn.commit()
			#print "COMMITTED"
		except Exception,ex:
			print ex
			print sqlStr
			print ""
			#assert 0
		#assert 0
		
		 
	def loadUser(self,dTweet):
		if self.userIDExists(dTweet["user"]["id"]):
			return

		dUser = dTweet["user"]
		strNewDescript = self.conn.escape_string(smart_str(dUser["description"]))
		strUserName = self.conn.escape_string(smart_str(dUser["name"]))
		strLocation = self.conn.escape_string(smart_str(dUser["name"]))
		sqlStr = "Insert into user_info (user_id, screen_name,name,friends,followers, description,image_url,location) values (%d,'%s','%s',%d,%d,\"%s\",'%s','%s')"
		try:
			sqlStr = sqlStr % (dUser["id"],dUser["screen_name"],strUserName,dUser["friends_count"],dUser["followers_count"],strNewDescript,dUser["profile_image_url"],strLocation)
		except Exception:
			strNewDescript=""
			sqlStr = sqlStr % (dUser["id"],dUser["screen_name"],strUserName,dUser["friends_count"],dUser["followers_count"],strNewDescript,dUser["profile_image_url"],strLocation)
		
		try:
			self.cursor.execute(sqlStr)
			self.conn.commit()
		except Exception:
			try:
				strNewDescript=""
				sqlStr = "Insert into user_info (user_id, screen_name,name,friends,followers, description,image_url,location) values (%d,'%s','%s',%d,%d,\"%s\",'%s','%s')"
				sqlStr = sqlStr % (dUser["id"],dUser["screen_name"],strUserName,dUser["friends_count"],dUser["followers_count"],strNewDescript,dUser["profile_image_url"],strLocation)
				self.cursor.execute(sqlStr)
				self.conn.commit()
			except Exception,ex:
				print sqlStr
				print ex
		
	def loadUserAndTweet(self,strD):
		lsStrD = strD.split("\n")
		bFirst=True
		print len(lsStrD)
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
				
			if bFirst:
				self.loadUser(dTweet)	
				bFirst=False
			
			self.loadTweet(dTweet)
			
	  
	def openAllFiles(self):

		lsFileNames = os.listdir(self.celeb_directory);
		print lsFileNames
		start=False
		for fileName in lsFileNames:
			if start==False and fileName.find("danfolger") == -1:
				 continue
			if fileName.find("danfolger") > -1:
				start=True
			print fileName
			print "*****************"
			if fileName==".DS_Store":
				continue
				
			#strJSON = open(self.celeb_directory+fileName).read()
			strFile = self.celeb_directory+fileName
			print strFile
			strD = open(strFile).read()
			self.loadUserAndTweet(strD)
	 
	def printBasicTweetInfo(self):
		
		fOut = open("/home/lisagandy/tweet_stats.csv","w")
		lsTweetIDS = self.getAllTweetIDS()		
		fields = ['tweet_id','num_followers','num_retweets']
		
		fDictWriter = csv.DictWriter(fOut,fields)
		fOut.write(','.join(fields)+'\n') #write header if not already there
	
		for tweet in lsTweetIDS:
			dTemp={}
			dTemp['tweet_id'] = tweet['tweet_id']
			dTemp['num_retweets'] = self.getNumRetweets(tweet['tweet_id'])['retweet_count']
			dTemp['num_followers'] = self.getNumFollowers(tweet['user_id'])['followers']
			fDictWriter.writerow(dTemp)
		fOut.close()
			

if __name__ == '__main__':
	ld = LoadDB()
	ld.printBasicTweetInfo();	