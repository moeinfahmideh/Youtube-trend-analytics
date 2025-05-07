
from .connection import get_connection

def create_raw_videos_table():
    cn = get_connection()

    query = """
    create table if not exists raw_videos(
    videoId     varchar     primary key,
    fetchedAt   timestamptz not null default now(),
    metadata    jsonb   not null
    )
"""
    cn.execute(query)
    cn.commit()


