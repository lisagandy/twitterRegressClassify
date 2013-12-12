import MySQLdb as mdb


class LoadTop5000:
	
	conn = None
	cursor = None
		
	def __init__(self):
		self.conn = mdb.connect('localhost', 'lisagandy', 'Chicago!!', 'TwitterCelebs');
		self.cursor = self.conn.cursor(mdb.cursors.DictCursor)	
	
	def update5000(self,user_id):
		sql = "Update user_info set top5000=1 where user_id=%s" % user_id
		self.cursor.execute(sql)
		self.conn.commit()
	
	
	def update5000Some(self,dRes,line):
		for res in dRes:
			if res['name'].strip().lower() == line.strip().lower():
				self.update5000(res['user_id'])
			else:
				print "PROBLEM WITH %s doesn't match %s" % (res['name'],line)
			
	
	def loadTop5000(self):
		f = open("/home/lisagandy/5000_celebs.txt")
		for i,line in enumerate(f.readlines()):
			 print i
			 line = self.conn.escape_string(line.strip())
			 sql = "Select user_id,name from user_info where name= '%s'" % line
			 #print sql
			 self.cursor.execute(sql)
			 dRes = self.cursor.fetchall()
			 if len(dRes) == 0:
				lastName = line.split(" ")[-1].strip()
				sql = "Select user_id,name from user_info where name like '%" + lastName + "';"
				self.cursor.execute(sql)
				dRes = self.cursor.fetchall()
				if len(dRes)==0:
					print "PROBLEM WITH %s" % line
				elif len(dRes)==1:
					self.update5000(dRes[0]['user_id'])
				else:
					self.update5000Some(dRes,line)
						
			 elif len(dRes) > 1:
				self.update5000Some(dRes,line)
		 	 elif len(dRes)==1:
				self.update5000(dRes[0]['user_id'])
			

if __name__ == '__main__':
	ld = LoadTop5000()
	ld.loadTop5000()