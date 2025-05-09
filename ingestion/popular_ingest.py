
import json
import sys
[sys.path.append(i) for i in ['.', '..']]
from db.connection import get_connection
from db.tables import create_raw_popular_videos_table, create_raw_channels_table
from fetch_popular import fetch_most_popular_ids, fetch_channels


def popular_videos_ingest(items):
    con = get_connection()
    create_raw_popular_videos_table()
    query = """
                insert into raw.raw_popular_vidoes (videoId, metadata) values (%s, %s::jsonb)
                ON CONFLICT (videoId)
                DO UPDATE SET
                metadata   = EXCLUDED.metadata,
                fetchedAt  = now()
            """
    for item in items:
        id = item['id']
        metadata = json.dumps(item)
        with con.cursor() as cur:
            cur.execute(query,(id,metadata))
    con.commit()
    con.close()

def channels_ingest(items):
    con = get_connection()
    create_raw_channels_table()
    query = """insert into raw.raw_channels (channelId, metadata) values (%s, %s::jsonb)
                ON CONFLICT (channelId)
                DO UPDATE SET
                metadata   = EXCLUDED.metadata,
                fetchedAt  = now()
            """
    for item in items:
        print(item)
        channelId = item['id']
        metadata = json.dumps(item)
        with con.cursor() as cur:
            cur.execute(query, (channelId,metadata))
    con.commit()
    con.close()
    return

def main():
    res_videos, nextPageToken = fetch_most_popular_ids()
    items = res_videos ['items']
    popular_videos_ingest(items)

    channel_ids = [item['snippet']['channelId'] for item in items]
    res_channels = fetch_channels(channel_ids)
    channel_items = res_channels['items']
    channels_ingest(channel_items)

    while len(channel_ids) < 1: # nextPageToken
        res_videos, nextPageToken = fetch_most_popular_ids(nextPageToken)
        items = res_videos ['items']
        popular_videos_ingest(items)
        channel_ids = [item['snippet']['channelId'] for item in items]
        res_channels = fetch_channels(channel_ids)
        channel_items = res_channels['items']
        channels_ingest(channel_items)
    

if __name__ == '__main__':
    main()