library('RMySQL')
library('DMwR')

con <- dbConnect(MySQL(), user="root", password="stuff0645", dbname="TwitterCelebs", host="localhost")

rt_outlier <- dbGetQuery(con, "SELECT * from outlier_info")
rt_not_outlier <- dbGetQuery(con,"Select * from not_outlier_info")
dbDisconnect(con)


rt = rbind(rt_outlier,rt_not_outlier)


rt[,"is_question"] = as.numeric(is.na(rt[,"is_question"])==F)
rt[,"has_url"] = as.numeric(is.na(rt[,"has_url"])==F)
rt[,"has_hashtag"] = as.numeric(is.na(rt[,"has_hashtag"])==F)
rt[,"has_video"] = as.numeric(is.na(rt[,"has_video"])==F)
rt[,"has_photo"] = as.numeric(is.na(rt[,"has_photo"])==F)
rt[,"has_mention"] = as.integer(is.na(rt[,"has_mention"])==F)

tid = rt[,"tweet_id"]
uid = rt[,"user_id"]
numf = rt[,"num_followers"]
isq = rt[,"is_question"]
hasu = rt[,"has_url"]
hash = rt[,"has_hashtag"]
hasv = rt[,"has_video"]
hasp = rt[,"has_photo"]
hasm = rt[,"has_mention"]

rt$is_outlier = factor(rt[,"is_outlier"])


#REGRESSION HERE
# 
# #plot(tid,y)
# 
#m = lm(y~tid+uid+numf+isq+hasu+hash+hasv+hasp+hasm)
#summary(m)
# 
#m = glm(y~tid+uid+numf+isq+hasu+hash+hasv+hasp+hasm,family=poisson())
#summary(m)
# hist(resid(m))

#BALANCE DATASET
newData <- SMOTE(is_outlier ~.,rt,perc.over=1500)

#CLASSIFICATION HERE
m = glm(newData$is_outlier~newData$num_followers+newData$is_question+newData$has_url+newData$has_hashtag+newData$has_video+newData$has_photo+newData$has_mention,family=binomial())

#GET CLASSIFICATION ERROR
pred<-ifelse(predict(m,type='response')>0.5,1,0)
table(pred,newData$is_outlier)