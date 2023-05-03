import requests
from xml.etree import ElementTree

def getPlayList(playlist_id):
    # get information of playlist from vibe music api
    playlist_url = "https://apis.naver.com/vibeWeb/musicapiweb/myMusic/myAlbums/" + str(playlist_id)
    playlist_headers = {
        'user-agent': 'github.com/yhg8423/vibe-api', 
        'referer': 'https://vibe.naver.com/mylist/'+str(playlist_id)
    }
    playlist_response = requests.get(playlist_url, headers=playlist_headers)
    
    if playlist_response.status_code == requests.codes.ok:
        playlist_text = playlist_response.text

        root = ElementTree.fromstring(playlist_text)
        num_of_tracks = int(root.find('result').find('myAlbums').find('myAlbum').find('trackCount').text)

        # get information of song in playlist from vibe music api
        tracks_info_url = "https://apis.naver.com/vibeWeb/musicapiweb/myMusic/myAlbum/"+ str(playlist_id) + '/tracks?start=1&display=' + str(num_of_tracks)
        tracks_info_response = requests.get(tracks_info_url, headers=playlist_headers)

        if tracks_info_response.status_code == requests.codes.ok:
            tracks_info_text = tracks_info_response.text

            root = ElementTree.fromstring(tracks_info_text)
            
            songs = dict()
            # get title and artists of each song
            for track in root.find('result').find('tracks').findall('track'): 
                title = track.find('trackTitle').text
                artists = track.find('artists').findall('artist')
                artistNames = []
                for artist in artists:
                    artistNames.append(artist.find('artistName').text)
                
                songs[title] = ', '.join(artistNames)
        else:
            raise Exception("vibe-api has a problem with http request.")
    else:
        raise Exception("vibe-api has a problem with http request.")

    return songs