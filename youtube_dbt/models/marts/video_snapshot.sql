{{ config(materialized='table') }}

select
    id, title, channelId, view_count, like_count, fetchedAt
    from clean.stg_videos
    order by view_count desc


