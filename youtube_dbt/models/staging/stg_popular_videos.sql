

{{ config(materialized='table')}}

select
videoId as id,
fetchedAt as  fetchedAt,
(metadata -> 'snippet' ->> 'title') as  title,
(metadata -> 'snippet' ->> 'channelId') as  channelId,
(metadata -> 'snippet' ->> 'categoryId') as  categoryId,
(metadata -> 'snippet' ->> 'description') as  descript,
(metadata -> 'snippet' ->> 'publishedAt') as  publishedAt,
(metadata -> 'statistics' ->> 'likeCount') ::int as  like_count,
(metadata -> 'statistics' ->> 'viewCount') ::int as  view_count,
(metadata -> 'statistics' ->> 'commentCount') ::int as  comment_count,
(metadata -> 'statistics' ->> 'favoriteCount') ::int as  favorite_count,
(metadata -> 'contentDetails' ->> 'caption')   caption,
(metadata -> 'contentDetails' ->> 'duration')  duration

from raw.raw_popular_vidoes