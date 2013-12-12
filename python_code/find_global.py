import numpy

text = open('all_tweets.csv').read()
lsLines = text.split("\n")


lsNum = []
for line in lsLines[1:]:
	try:
		if (int(line)>0):
			lsNum.append(int(line))
	except Exception,ex:
		continue

median = numpy.median(lsNum)
lsNewNum=[]
for num in lsNum:
	lsNewNum.append(abs(num-median))

print numpy.mean(lsNewNum)
#you get 466

# lsNum = []
# for line in lsLines[1:]:
# 	try:
# 		if (int(line)>0):
# 			lsNum.append(int(line))
# 	except Exception,ex:
# 		continue
# 
# lsNum = list(set(lsNum))
# med = numpy.median(lsNum)
# lsNewNum = []
# for num in lsNum:
# 	lsNewNum.append(abs(num-med))
# 
# madE = numpy.median(lsNewNum)* 1.483 * 2
# print madE
# 
# upperRange = madE + med
# print upperRange

#upper range is 21
