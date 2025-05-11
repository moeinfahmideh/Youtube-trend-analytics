{{ config(materialized='table') }}

WITH ch_avg AS (
  SELECT
    channelId                AS channel_id,
    AVG(view_count)          AS avg_channel_views,
    STDDEV_POP(view_count)   AS stddev_channel_views
  FROM {{ ref('stg_popular_videos') }}
  GROUP BY 1
)

SELECT
  v.id                      AS video_id,
  v.title,
  v.view_count,
  a.avg_channel_views,
  a.stddev_channel_views,
  ROUND((v.view_count - a.avg_channel_views) / NULLIF(a.stddev_channel_views,0) , 2)
                            AS z_score
FROM {{ ref('stg_popular_videos') }} v
JOIN ch_avg a
  ON v.channelId = a.channel_id
WHERE (v.view_count - a.avg_channel_views) > a.stddev_channel_views  
ORDER BY z_score DESC
