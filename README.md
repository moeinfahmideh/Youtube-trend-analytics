# 📺 YouTube Analytics Pipeline — 30-Day Rolling Window

**Ingest, transform, and surface YouTube metrics: end-to-end, policy-compliant, fully automated with Airflow + dbt.**

| Layer        | Tech                         |
| ------------ | ---------------------------- |
| Orchestrator | **Apache Airflow 2**         |
| Ingestion    | Python (YouTube Data API v3) |
| Storage      | PostgreSQL 15                |
| Transform    | dbt 1.9 (staging + marts)    |
| Quality      | dbt tests                    |
| Viz          | Streamlit (sample dashboard) |

---

## 🚀 Quick Start

```bash
git clone https://github.com/<your-handle>/youtube-pipeline.git
cd youtube-pipeline

# 1 — create + activate virtual env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2 — supply credentials
cp .env.example .env                    # add YouTube API key + Postgres creds
cp profiles.example.yml profiles.yml    # adjust if needed

# 3 — initialise Airflow inside repo
export AIRFLOW_HOME="$(pwd)/airflow"
airflow db init
airflow users create --username admin --role Admin \
                     --firstname you --lastname you --email you@example.com

# 4 — run the pipeline once
airflow dags trigger youtube_daily_pipeline   # or run ingestion/raw_ingest.py manually

# 5 — start scheduler + web UI (port 8080) and watch tasks turn 🟩
airflow scheduler   &   airflow webserver   &
```

Default schedule: every day at 21:50 UTC. The pipeline keeps exactly the last 30 days of raw data.

---

## 🗺️ Project Tour

```md
youtube-pipeline/
├── airflow/ ← Airflow home (dags/, logs/, airflow.db)
│ └── dags/
│ └── youtube_pipeline.py
├── ingestion/ ← Python ETL scripts
│ ├── fetch_general_videos.py
│ ├── fetch_popular.py
│ ├── popular_ingest.py
│ └── raw_ingest.py
├── db/ ← Connection helpers + table DDL
├── youtube_dbt/ ← dbt project (staging + marts + tests)
│ └── models/
│ ├── staging/
│ └── marts/
├── visualize/ ← Streamlit dashboard (optional)
└── docs/ ← diagrams, screenshots, policy doc
```

---

## Data Models

| Layer       | Table(s)                                                                                      | Key idea                                                    |
| ----------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Raw**     | `raw.raw_videos`, `raw.raw_popular_videos`, `raw.raw_channels`                                | JSON blobs exactly as returned by the API (rolling 30 days) |
| **Staging** | `clean.stg_videos`, `clean.stg_channels`, `clean.stg_popular_videos`                          | Flattened columns, typed; dbt `unique` / `not_null` tests   |
| **Marts**   | `video_snapshot`, `channel_summary`, `video_viral_index`, `underdog_videos`, `channel_growth` | Viral-index leaderboard, rising channels, growth velocity   |

Generate full docs:

```bash
cd youtube_dbt
dbt docs generate && dbt docs serve
```

---

## Compliance & Attribution

This project adheres to the **YouTube Data API v3 Terms of Service**. In particular:

- **No raw data republishing**  
  • We never store or expose the full JSON payloads beyond our internal `raw` schema.  
  • Only **derived** or **aggregated** metrics (e.g. total views, viral-index ratios) appear in our public marts.

- **30-day retention window**  
  • Raw API responses are **overwritten or purged** once they are older than 30 days, ensuring we never keep stale public stats.  
  • Our Airflow DAG enforces this rolling window automatically each night.

- **API key security**  
  • The YouTube API key is **not** checked into version control—credentials live in a local `.env` file.  
  • We recommend rotating keys periodically via the Google Cloud Console.

- **Attribution**  
  • All charts and dashboards include a visible “Powered by YouTube” link back to the official site.  
  • YouTube’s logos and trademarks are used only in accordance with the [brand guidelines](https://developers.google.com/youtube/branding).

- **No endorsement implied**  
  • This project is a **personal demonstration** and is **not** affiliated with, sponsored by, or endorsed by Google LLC.

For full details on permitted uses, data retention, quota limits, and branding requirements, see `docs/youtube_data_policy.md`.
