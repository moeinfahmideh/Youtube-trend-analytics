
import json
import os
from dotenv import load_dotenv
from db.connection import get_connection
from db.tables import create_raw_videos_table
from ingestion.fetch_general_videos import fetch_ids_page, fetch_video_metadata

load_dotenv()

def insert_raw_videos(cn, items):
    
    query = """insert into raw.raw_videos (videoId, metadata) values (%s, %s::jsonb) 
                ON CONFLICT (videoId)
                DO UPDATE SET
                metadata   = EXCLUDED.metadata,
                fetchedAt  = now() """
    for item in items:
        videoId = item['id']
        md = json.dumps(item)
        with cn.cursor() as cur:
            cur.execute(query,(videoId,md))
    cn.commit()

def main():
    con = get_connection()
    create_raw_videos_table()
    all_ids = []
    token = None
    while True:
        ids, token = fetch_ids_page(token)
        all_ids.append(ids)

        if len(all_ids) > 2:
            break

    for batch in all_ids:
        data = fetch_video_metadata(batch)
        print(data.keys())
        
        items = data['items']
        insert_raw_videos(con, items)
        print(f"Wrote {len(items)} videos.")

    con.close()


if __name__ == "__main__":
    main()
