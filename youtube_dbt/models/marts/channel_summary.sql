{{ config(materialized='table') }}

select 
    channelId,
    count(*) as video_count,
    sum(view_count) as total_views,
    sum(like_count) as total_likes,
    avg(view_count) as avg_views_per_video,
    Max(fetchedAt) as latest_update

from clean.stg_videos
group by 1
order by total_views desc

