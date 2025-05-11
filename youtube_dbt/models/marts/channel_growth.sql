{{ config(materialized='table') }}

WITH snapshots AS (
  SELECT
    id           AS channel_id,
    subscriber_count,
    DATE(fetchedAt) AS snap_date
  FROM {{ ref('stg_channels') }}
),

first_last AS (
  SELECT
    channel_id,
    MIN(snap_date) AS first_date,
    MAX(snap_date) AS last_date
  FROM snapshots
  GROUP BY 1
),

growth AS (
  SELECT
    f.channel_id,
    f.subscriber_count           AS start_subs,
    l.subscriber_count           AS end_subs,
    l.subscriber_count - f.subscriber_count AS delta_subs,
    l.snap_date - f.snap_date    AS days_elapsed
  FROM snapshots f
  JOIN first_last fl
    ON f.channel_id = fl.channel_id
   AND f.snap_date  = fl.first_date
  JOIN snapshots l
    ON l.channel_id = fl.channel_id
   AND l.snap_date  = fl.last_date
)

SELECT
  channel_id,
  start_subs,
  end_subs,
  delta_subs,
  ROUND(delta_subs::numeric / NULLIF(days_elapsed,0), 2) AS avg_daily_gain
FROM growth
ORDER BY avg_daily_gain DESC
