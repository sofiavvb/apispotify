from requests import post, get
from dotenv import load_dotenv
import os
import base64
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_artist(token, artist_name):
    url =  "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    #artist not found 
    if len(json_result) == 0:
        return None
    return json_result[0]

def get_artist_albums(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?market=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def get_album_tracks(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks?&market=US&limit=50"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

def search_album(token, album_name):
    url =  "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={album_name}&type=album&limit=1&market=US"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["albums"]["items"]
    #album not found 
    if len(json_result) == 0:
        return None
    return json_result[0]

def save_tracks(token):
    #save in a json file all ts main discography
    albums_taylor = ["THE TORTURED POETS DEPARTMENT THE ANTHOLOGY", "1989 (Taylor's Version) [Deluxe]",
                    "Speak Now (Taylor's Version)", "Midnights (The Til Dawn Edition)", "Red (Taylor's Version)",
                    "Fearless (Taylor's Version)", "evermore (deluxe version)", "folklore (deluxe version)", "Lover",
                    "reputation", "Taylor Swift (Deluxe)"]
    
    all_tracks_data = {}
    for album in albums_taylor:
        # get album id
        id = search_album(token, album)["id"]
        # get album tracks
        tracks = get_album_tracks(token, id)

        all_tracks_data[album] = tracks

    with open("tracks.json", "w") as file:
        json.dump(all_tracks_data, file, indent=4)

def main():
    token = get_token()
    save_tracks(token)

if __name__ == "__main__":
    main()
