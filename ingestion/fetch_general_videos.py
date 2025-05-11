import os, requests
from dotenv import load_dotenv

load_dotenv()
API_key = os.getenv("API_KEY")

def fetch_ids_page(nextPageToken=None):
    api = 'https://www.googleapis.com/youtube/v3/search'
    params ={
    "part" : "id",
    "type" : "video",
    "maxResults" : 50,
    "publishedAfter" : "2025-05-01T00:00:00Z",
    "key" : API_key
}
    if nextPageToken:
        params['nextPageToken'] = nextPageToken

    response = requests.get(api, params=params, timeout=10)
    response.raise_for_status()               # error if not 200
    data = response.json()
    ids = [item['id']['videoId'] for item in data['items']]
    nextPageToken = data['nextPageToken']
    return ids, nextPageToken

def fetch_video_metadata(batch):
    api = 'https://www.googleapis.com/youtube/v3/videos'
    id_param = ','.join(batch) # turning a list to comma seprated format, required for API
    params = {
        'part' : "snippet,contentDetails,statistics",
        'id' : batch,
        'key': API_key
    }

    response = requests.get(api,params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    return data



    
