
{{ config(materialized='table') }}

select

fetchedAt   as  fetchedAt,
metadata ->> 'id' as id,
(metadata -> 'snippet' ->> 'title' ) as title,
(metadata -> 'snippet' ->> 'description') as descript,
(metadata -> 'snippet' ->> 'publishedAt') as publishedAt,
(metadata -> 'statistics' ->> 'likeCount')::int as like_count,
(metadata -> 'statistics' ->> 'viewCount')::int as view_count,
(metadata -> 'statistics' ->> 'favoriteCount')::int as favorite_count,
(metadata -> 'contentDetails' ->> 'caption') as caption,
(metadata -> 'contentDetails' ->> 'duration') as duration


from raw.raw_videos
