{{config(materialized='table')}}
--- returns viral index: video view count / channel subscriber count

with vid as (
    select
        id as video_id,
        title,
        channelId as channel_id,
        like_count,
        view_count
    from {{ref('stg_popular_videos')}}
),

chnl as (
    select
        id as channel_id,
        subscriber_count,
        view_count
    from {{ref('stg_channels')}}
)

select
    v.video_id,
    v.title,
    v.channel_id,
    v.view_count,
    c.subscriber_count,
    case 
        when    c.subscriber_count = 0 then v.view_count
        else    round((v.view_count::decimal / c.subscriber_count)::numeric, 2)
    end as viral_index

from vid v
left join chnl c 
using (channel_id)

order by viral_index desc, v.view_count desc
