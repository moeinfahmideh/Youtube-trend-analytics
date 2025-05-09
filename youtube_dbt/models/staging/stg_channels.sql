
{{ (config(materialized='table'))}}

select
channelId as id,
fetchedAt as fetchedAt,
(metadata -> 'snippet' ->> 'title') as title,
(metadata -> 'snippet' ->> 'country') as country, 
(metadata -> 'snippet' ->> 'customUrl') as customUrl, 
(metadata -> 'snippet' ->> 'description') as descript, 
(metadata -> 'snippet' ->> 'publishedAt') as publishedAt, 
(metadata -> 'statistics' ->> 'viewCount') ::bigint as view_count, 
(metadata -> 'statistics' ->> 'videoCount') ::bigint as video_count, 
(metadata -> 'statistics' ->> 'subscriberCount') ::bigint as subscriber_count, 
(metadata -> 'statistics' ->> 'hiddenSubscriberCount') as hiddenSubscriber_count,
(metadata -> 'contentDetails' ->> 'relatedPlaylists') as relatedPlaylists

from raw.raw_channels