{{ config(materialized='table') }}


select
    
    title,
    view_count,
    (like_count:: numeric/view_count) as like_view_ratio,
    (comment_count::numeric/view_count) as comment_view_ratio


from clean.stg_videos

