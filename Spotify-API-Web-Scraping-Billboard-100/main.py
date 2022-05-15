import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = "ENTER YOUR CLIENT ID "
CLIENT_SECRET = " ENTER YOUR CLIENT SECRET "

date = input(f"Which year you want to travel to? "
                       f"Type the date in this format (YYYY-MM-DD): ")

response = requests.get(url=f"{URL}/{date}/")
billiboard_web_page = response.text

soup = BeautifulSoup(billiboard_web_page, "html.parser")

song_titles = soup.select(selector="li h3", id="title-of-a-story")
song_titles = song_titles[0:100]
song_names = [song.get_text().strip() for song in song_titles]
print(song_names)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris = []
year = date.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
