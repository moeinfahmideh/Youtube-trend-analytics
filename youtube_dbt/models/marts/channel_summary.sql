{{ config(materialized='table') }}

with vids as (
select
    channelId as channel_id,
    count(*) as video_count,
    sum(view_count) as total_views,
    sum(like_count) as total_likes,
    avg(view_count) as avg_views_per_video,
    Max(date(fetchedAt)) as latest_update

from clean.stg_videos
group by 1
order by total_views desc
)
select 
    c.title,
    v.video_count,
    v.total_views,
    v.total_likes, 
    avg_views_per_video,
    latest_update

from vids v 
left join {{ ref('stg_channels') }} c 
on v.channel_id = c.id

