-- create table tweet_question(`tweet_id` bigint(20) unsigned not null, primary key (`tweet_id`), constraint `tweet_id_7` foreign key (`tweet_id`) references `tweets` (`tweet_id`));

-- CREATE TABLE hashtags(
-- 	`tweet_id` bigint(20) unsigned NOT NULL,
-- 	`hashtag` varchar(50) NOT NULL,
-- 	PRIMARY KEY (`tweet_id`,`hashtag`),
-- 	CONSTRAINT `tweet_id_1` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`)
-- 	)

-- CREATE TABLE urls(
-- 	`tweet_id` bigint(20) unsigned NOT NULL,
-- 	`url` varchar(500) NOT NULL,
-- 	PRIMARY KEY (`tweet_id`,`url`),
-- 	CONSTRAINT `tweet_id_2` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`)
-- 	);
-- 
-- CREATE TABLE media(
-- 	`tweet_id` bigint(20) unsigned NOT NULL,
-- 	`media_url` varchar(500) NOT NULL,
-- 	PRIMARY KEY (`tweet_id`,`media_url`),
-- 	CONSTRAINT `tweet_id_3` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`)
-- 	);

CREATE TABLE mentions(
	`tweet_id` bigint(20) unsigned NOT NULL,
	`mention` varchar(500) NOT NULL,
	PRIMARY KEY (`tweet_id`,`mention`),
	CONSTRAINT `tweet_id_4` FOREIGN KEY (`tweet_id`) REFERENCES `tweets` (`tweet_id`)
	);





-- CREATE TABLE user_info (
--   `user_id` bigint(20) unsigned NOT NULL,
--   `screen_name` varchar(25) NOT NULL DEFAULT ``,
--   `name` varchar(250) NOT NULL DEFAULT ``,
--   `followers` bigint(10) unsigned NOT NULL DEFAULT `0`,
--   `friends` int(10) unsigned DEFAULT NULL,
--   `description` varchar(700) NOT NULL DEFAULT ``,
--   `image_url` varchar(500) NOT NULL DEFAULT ``,
--   `last_update` datetime DEFAULT NULL,
--   `location` varchar(500) NOT NULL DEFAULT ``,
--   PRIMARY KEY (`user_id`)
-- ) 

-- CREATE TABLE tweets (
--   `tweet_id` bigint(20) unsigned NOT NULL,
--   `tweet_text` varchar(1000) DEFAULT NULL,
--   `created_at` datetime DEFAULT NULL,
--   `geo_lat` decimal(10,5) DEFAULT NULL,
--   `geo_long` decimal(10,5) DEFAULT NULL,
--   `user_id` bigint(10) unsigned DEFAULT NULL,
--   `tweet_url` varchar(200) DEFAULT NULL,
--   `retweet_count` int(10) DEFAULT NULL,
--   `original_tweet_id` bigint(20) DEFAULT NULL,
--   PRIMARY KEY (`tweet_id`),
--   KEY `user_id` (`user_id`),
--   KEY `idx_created_at` (`created_at`),
--   KEY `retweet_index` (`retweet_count`),
--   KEY `orig_tweet_index` (`original_tweet_id`),
--   CONSTRAINT `tweets_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_info` (`user_id`)
-- ) 
