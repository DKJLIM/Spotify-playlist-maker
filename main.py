import bs4
import requests
import spotipy

date = input("enter the year you want to travel to (YYYY-MM-DD): ")
URL = f"https://www.billboard.com/charts/hot-100/{date}/"

response = requests.get(url=URL)
HTML = response.text

soup = bs4.BeautifulSoup(HTML, "html.parser")

song_artist = []
song_title = []

result = soup.find_all('div', class_='o-chart-results-list-row-container')
for res in result:
    song_names = res.find('h3').text.strip()
    song_title.append(song_names)
    artist_names = res.find('h3').find_next('span').text.strip()
    song_artist.append(artist_names)


############Spotify content###########

sp = spotipy.Spotify(
    auth_manager=spotipy.oauth2.SpotifyOAuth(
        client_id="insert your client_id",
        client_secret="insert your client secret",
        redirect_uri="https://example.com",
        scope="playlist-modify-private",
        show_dialog='true',
        cache_path='token.txt'
    ))


user_name = sp.current_user()["display_name"]
user_id = sp.current_user()["id"]

#some additional code

song_urls = []
for song, artist in zip(song_title, song_artist):
    items = sp.search(q=f"track: {song} artist: {artist}", type="track")["tracks"]["items"]
    if len(items) > 0:
        song_urls.append(items[0]["uri"])


playlist_id = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)["id"]

sp.playlist_add_items(playlist_id=playlist_id, items=song_urls)
print(song_urls)

playlist=sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_urls)