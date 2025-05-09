import os
import requests

from dotenv import load_dotenv
load_dotenv()

def fetch_most_popular_ids(nextPageToken= None):
    api = 'https://www.googleapis.com/youtube/v3/videos'
    params = {
        'part': 'snippet,contentDetails,statistics',
        'chart' : 'mostPopular',
        'regionCode' : 'US',
        'maxResults' : 50,
        'key' : os.getenv('API_KEY')
    }
    if nextPageToken:
        params['nextPageToken'] = nextPageToken

    res = requests.get(api,params=params, timeout=10)
    
    res = res.json()
    nextPageToken = res['nextPageToken']
    return res, nextPageToken

def fetch_channels(batch):
    api = 'https://www.googleapis.com/youtube/v3/channels'
    params = {
        'part' : 'snippet,contentDetails, Statistics',
        'id' : batch,
        'key' : os.getenv('API_KEY')
    }
    res = requests.get(api,params=params, timeout=10)
    res = res.json()
    return res

def main():
    channel_ids = []
    res, nextPageToken = fetch_most_popular_ids()
    items = res ['items']
    ids = [item['snippet']['channelId'] for item in items]
    channel_ids.append(ids)
    fetch_channels(channel_ids[0])
    while len(channel_ids) < 1: # nextPageToken
        res, nextPageToken = fetch_most_popular_ids(nextPageToken)
        items = res ['items']
        ids = [item['snippet']['channelId'] for item in items]
        channel_ids.append(ids)

if __name__ == "__main__":
    main()