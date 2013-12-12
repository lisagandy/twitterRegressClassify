-- create table not_outlier_info(
-- 	`tweet_id` bigint(20) unsigned NOT NULL,
-- 	`user_id` bigint(20),
-- 	`num_followers` bigint(10) unsigned,
-- 	`is_question` boolean,
-- 	`has_url` boolean,
-- 	`has_hashtag` boolean,
-- 	`has_video` boolean,
-- 	`has_photo` boolean,
-- 	`has_mention` boolean,
-- 	`is_outlier` boolean	
-- 	);
-- 
-- --get non outlier tweet_ids from sample	
-- insert into not_outlier_info (`tweet_id`) Select tweet_id from tweets where tweet_id not in (Select tweet_id from outlier_info);
-- 	
--update the user ids
update not_outlier_info set user_id=(Select user_id from tweets where tweets.tweet_id=not_outlier_info.tweet_id); 
	
--update num followers
update not_outlier_info set num_followers=(Select followers from user_info where not_outlier_info.user_id=user_info.user_id);

--update if question or not
update not_outlier_info set is_question=1 where tweet_id=(Select tweet_id from tweets where tweets.tweet_id=not_outlier_info.tweet_id and tweets.tweet_text like "%?%");
update not_outlier_info set is_question=1 where tweet_id=(Select tweet_id from tweets where tweets.tweet_id=not_outlier_info.tweet_id and tweets.tweet_text like "%?");
	
--update url
update not_outlier_info set has_url=1 where (Select Count(*) from urls where urls.tweet_id=not_outlier_info.tweet_id) > 0;

--update hashtags	
update not_outlier_info set has_hashtag=1 where (Select Count(*) from hashtags where hashtags.tweet_id=not_outlier_info.tweet_id) > 0;	

--update mentions	
update not_outlier_info set has_mention=1 where (Select Count(*) from mentions where mentions.tweet_id=not_outlier_info.tweet_id) > 0;	
	
--all media are photos right now so update media as having photos
update not_outlier_info set has_photo=1 where (Select Count(*) from media where media.tweet_id=not_outlier_info.tweet_id) > 0;
	
--update urls so type media is more nuanced
Update urls set type_media='video' where url like "%youtube%";
Update urls set type_media='video' where url like "%youtu.be%";
Update urls set type_media='video' where url like "%video%";
Update urls set type_media='video' where url like "%watch%";
Update urls set type_media='video' where url like "%twitvid%";
Update urls set type_media='video' where url like "%on.vh1.com%";

Update urls set type_media='photo' where url like "%twitpic%";
Update urls set type_media='photo' where url like "%image%";
Update urls set type_media='photo' where url like "%photo%";
Update urls set type_media='photo' where url like "%img%";
Update urls set type_media='photo' where url like "%jpg%";
Update urls set type_media='photo' where url like "%gif%";
Update urls set type_media='photo' where url like "%png%";
Update urls set type_media='photo' where url like "%pic%";

--update photos and videos from urls now
update not_outlier_info set has_photo=1 where (Select Count(*) from urls where urls.tweet_id=not_outlier_info.tweet_id and type_media='photo') > 0;
update not_outlier_info set has_photo=1 where (Select Count(*) from urls where urls.tweet_id=not_outlier_info.tweet_id and type_media='video') > 0;

update not_outlier_info set is_outlier=0;
	
-- SELECT tweet_id,user_id,num_followers,has_mention,is_question,has_url,has_hashtag, has_video,has_photo,is_outlier from not_outlier_info INTO OUTFILE '/home/lisagandy/not_outlier_table.csv'
-- 	    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
-- 	    LINES TERMINATED BY '\n';
