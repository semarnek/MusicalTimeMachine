import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint

SPOTIPY_CLIENT_ID = YOUR_CLIENT_ID
SPOTIPY_CLIENT_SECRET = YOUR_CLIENT_SECRET
date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = "https://www.billboard.com/charts/hot-100/" + date
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")
songs = soup.find_all("li", class_="lrv-u-width-100p")
song_list = {}
count = 0
for song in songs:
    if count % 2 == 0:
        song_ = song.getText().split("\n")[8].split("\t")[5]
        artist_ = song.getText().split("\n")[13].split("\t")[1]
        song_list[song_] = artist_
    count += 1


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://www.instagram.com/",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

auth= {
    "Authorization":"Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}
song_uris = []


for song in song_list:
    result = sp.search(q=f"track:{song} artist:{song_list[song]}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

