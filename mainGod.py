import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv, find_dotenv
import os

# ---------- api ----------
load_dotenv(find_dotenv())
client_id = (os.getenv('YOUR_CLIENT_ID'))
client_secret = (os.getenv('YOUR_CLIENT_SECRET'))

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# ---------- main ----------
def find_track_info(track_name):
    track_selection = []
    search_results = sp.search(q=track_name, type='track', limit=50)

    if search_results['tracks']['items']:
        for idx, track in enumerate(search_results['tracks']['items']):
            if idx < 20:
                track_selection.append(track)
                print(f"{idx+1}. {track['name']} - {', '.join([artist['name'] for artist in track['artists']][:3])}")

        if track_selection:
            selected_idx = int(input("Выберите номер трека для получения подробной информации: "))

            if 0 < selected_idx <= 20:
                selected_track = track_selection[selected_idx-1]

                release_date = selected_track['album']['release_date']
                artist_id = selected_track['artists'][0]['id']
                track_genre = sp.artist(artist_id)['genres']

                output = (
                    f"Имя артиста: {', '.join([artist['name'] for artist in selected_track['artists']][:3])}\n"
                    f"ID артиста: {artist_id}\n"
                    f"Название трека: {selected_track['name']}\n"
                    f"Ссылка на трек: {selected_track['external_urls']['spotify']}\n"
                    f"Дата выхода трека: {release_date}\n"
                    f"Жанры: {', '.join(track_genre[:10])}\n"
                    f"Популярность: {selected_track['popularity']}"
                )
                
                print(output)

            else:
                print("Неверный номер трека, попробуйте еще раз.")

        else:
            print("Не найдено подходящих треков для введенного запроса.")

    else:
        print("Не найдено подходящих треков для введенного запроса.")


# ---------- find track----------
track_name = input("Введите название трека: ")
tracks = find_track_info(track_name)