# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 22:54:35 2020

@author: trevo
"""

#Setting Environment variables
import os
os.environ['SPOTIPY_CLIENT_ID']='1e47c40f3ed046d1aa8b09d661f83910'
os.environ['SPOTIPY_CLIENT_SECRET']='0fdcfca5d43d481ea1f04607a51f1657'

#Relevant/Used modules
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm_notebook

#John mayers uri + specifying credentials
mayer_uri = 'spotify:artist:0hEurMDQu99nJRq8pTxO14'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

#Macro for reproducibility - Change for artist of interest
artist = 'John Mayer'

#Getting John Mayer's Related Artists included in a list
related = spotify.artist_related_artists('0hEurMDQu99nJRq8pTxO14')

relatedlist = []
for person in related['artists']:
    relatedlist.append(person['name'])
relatedlist.insert(0, artist)
relatedlist
####### FUNCTIONS TO RETRIEVE DATA DESIRED ##########
#Get all the tracks for the list of artists
def artist_tracks(artists):
    '''
    Takes a list of artist names, iterates through their Spotify albums, checks for 
    duplicate albums, then appends all the tracks in those albums to a list of lists
    '''
    # Each list in this list will be a track and its features
    tracks = []
    for artist in tqdm_notebook(artists):
        
        # Get the artist URI (a unique ID)
        artist_uri = spotify.search(artist)['tracks']['items'][0]['artists'][0]['uri']

        # Spotify has a lot of duplicate albums, but we'll cross-reference them with this list to avoid extra loops
        album_checker = []
        
        # The starting point of our loop of albums for those artists with more than 50
        n = 0
        
        # Note the album_type = 'album'. This discounts singles, compilations and collaborations
        while len(spotify.artist_albums(artist_uri, album_type = 'album', limit=50, offset = n)['items']) > 0:
            
            # Avoid overloading Spotify with requests by assigning the list of album dictionaries to a variable
            dict_list = spotify.artist_albums(artist_uri, album_type = 'album', limit=50, offset = n)['items']
            for i, album in tqdm_notebook(enumerate(dict_list)):

                # Add the featured artists for the album in question to the checklist
                check_this_album = [j['name'] for j in dict_list[i]['artists']]
                # And the album name
                check_this_album.append(dict_list[i]['name'])
                # And its date
                check_this_album.append(dict_list[i]['release_date'])

                # Only continue looping if that album isn't in the checklist
                if check_this_album not in album_checker:
                    
                    # Add this album to the checker
                    album_checker.append(check_this_album)
                    # For every song on the album, get its descriptors and features in a list and add to the tracklist
                    tracks.extend([[artist, album['name'], album['uri'], song['name'],
                      album['release_date']] + list(spotify.audio_features(song['uri'])[0].values()) 
                                   for song in spotify.album_tracks(album['uri'])['items']])
            
            # Go through the next 50 albums (otherwise we'll get an infinite while loop)
            n += 50
    return tracks

#Takes output from above function and formats it into a Pandas df
def df_tracks(tracklist):
    '''
    Takes the output of artist_tracks (i.e. a list of lists),
    puts it in a dataframe and formats it.
    '''
    df = pd.DataFrame(tracklist, columns=['artist',
     'album_name',
     'album_uri',
     'track',
     'release_date'] + list(spotify.audio_features('7tr2za8SQg2CI8EDgrdtNl')[0].keys()))

    df.rename(columns={'uri':'song_uri'}, inplace=True)

    df.drop_duplicates(subset=['artist', 'track', 'release_date'], inplace=True)

    # Reorder the cols to have identifiers first, auditory features last
    cols = ['artist', 'album_name', 'album_uri', 'track', 'release_date', 'id', 'song_uri', 'track_href',
     'analysis_url', 'type', 'danceability', 'energy', 'key',  'loudness', 'mode', 'speechiness',
     'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']
    df = df[cols]
    return df

#Sample list to try functions - Successful
sample = ['John Mayer']
songs = artist_tracks(sample)
JMSongs = df_tracks(songs)
songs
#Getting all the songs from all the related artists including JM
artist_songs = artist_tracks(relatedlist)
artist_songs = df_tracks(artist_songs)
for col in artist_songs.columns:
    print(col, type(col))

#Getting the individual popularities for each individual track
popularity = []
for i in artist_songs.song_uri:
    track_info = spotify.track(i)
    popularity.append(track_info['popularity'])
    
all_song_uris = artist_songs['song_uri'].to_list()

#Merging lists of song uris and popularity to create a common key between 'popularity' and 'artist_songs' before export
popularity = pd.DataFrame(list(zip(all_song_uris, popularity)), columns =['song_uri', 'popularity'])
popularity    

#Exporting to excel - go to R
artist_songs.to_excel(r'C:\Users\trevo.DESKTOP-Q3G2N9L\Documents\Resume Materials\Syneos Health\Case Study Scripts\ArtistData.xlsx')
popularity.to_excel(r'C:\Users\trevo.DESKTOP-Q3G2N9L\Documents\Resume Materials\Syneos Health\Case Study Scripts\Popularity.xlsx')


#Unused code - Testing functions, getting song popularity, etc.
#JM = spotify.artist_albums('spotify:artist:0hEurMDQu99nJRq8pTxO14', album_type = 'album', limit = 1)
#JM['items'][0]['name'] #The Search for Everything


#for i in relatedlist:
#    artist_uri = spotify.search(i)['tracks']['items'][0]['artists'][0]['uri']
#    audio = spotify.artist(artist_uri)
#    print(audio['name'])
#    print(audio['popularity'])
    
#example = spotify.search('casual sabotage', type = 'track', limit = 1)
#exampleuri = example['tracks']['items'][0]['uri']
#examplepop = spotify.track('00gvX9sFwh19OH88f4v4jW')
#examplepop['popularity']

#example['tracks']['items'][0]['artists'][0]['name']



















