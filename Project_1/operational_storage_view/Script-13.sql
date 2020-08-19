
create view rbc_views_analitics as(
select ondis.hash_key technical_hk1,
		ondis.hash_diff technical_hd1,
		orns.hash_key technical_hk2, 
		orns.hash_diff technical_hd2,
		ondis.publication_date news_publication_date,
		ondis.header news_header,
		ondis.topic news_topic,
		orns.`date` date_and_time,
		orns.date_ts date_and_time_ts,
		orns.views news_views
		from os_news_detailed_info_sha_1 ondis
	join os_rbc_news_views_sha_1 orns
		on ondis.hash_key=orns.hash_key
			group by orns.hash_diff);
		
		
select*from rbc_views_analitics;

show tables;




