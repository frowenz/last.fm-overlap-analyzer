import requests
import csv
import os
from dotenv import load_dotenv
load_dotenv()

LAST_FM_API_URL = 'https://ws.audioscrobbler.com/2.0/'

def get_user_top_tracks(username, api_key):
    url = LAST_FM_API_URL
    payload = {
        'method': 'user.getTopTracks',
        'user': username,
        'api_key': api_key,
        'format': 'json',
        'limit': 3000,  # adjust this value to fetch more or fewer tracks
        'page': 1
    }
    response = requests.get(url, params=payload)
    data = response.json()

    top_tracks = {}
    for track in data['toptracks']['track']:
        title = track['name']
        artist = track['artist']['name']
        playcount = int(track['playcount'])
        top_tracks[(title, artist)] = playcount

    return top_tracks

def find_overlap(user1_data, user2_data):
    overlap = {}
    for track, playcount in user1_data.items():
        if track in user2_data:
            min_playcount = min(playcount, user2_data[track])
            if min_playcount >= 5:
                overlap[track] = min_playcount

    sorted_overlap = dict(sorted(overlap.items(), key=lambda item: item[1], reverse=True))

    # Return the top 100 shared songs
    # return dict(list(sorted_overlap.items())[:100])

    return dict(list(sorted_overlap.items()))


def write_csv(filename, overlap_data):
    with open(os.path.join("downloads", filename), 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Song', 'Artist', 'Min_Listens_Either_User'])
        for (title, artist), min_listeners in overlap_data.items():
            csv_writer.writerow([title, artist, min_listeners])
