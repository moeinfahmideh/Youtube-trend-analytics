
from db.connection import get_connection

def create_raw_videos_table():
    cn = get_connection()
    query = "create schema if not exists raw;"
    cn.execute(query)
    cn.commit()

    query = """
    create table if not exists raw.raw_videos(
    videoId     varchar     primary key,
    fetchedAt   timestamptz not null default now(),
    metadata    jsonb   not null
    )
"""
    cn.execute(query)
    cn.commit()

def create_raw_popular_videos_table():
    cn = get_connection()
    query = 'create schema if not exists raw'
    cn.execute(query)
    cn.commit()

    query = """
        create table if not exists raw.raw_popular_vidoes(
            videoId     varchar     primary key,
            fetchedAt   timestamptz not null default now(),
            metadata    jsonb   not null
        )
        """
    cn.execute(query)
    cn.commit()
    cn.close()

def create_raw_channels_table():
    cn = get_connection()
    query = 'create schema if not exists raw'
    cn.execute(query)
    cn.commit()
    query = """
        create table if not exists raw.raw_channels(
            channelId   varchar primary key,
            fetchedAt   timestamptz not null default now(),
            metadata     jsonb   not null
        )
    """
    cn.execute(query)
    cn.commit()
    cn.close()
