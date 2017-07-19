import sys
import os

import requests
import soundcloud


soundcloud_client = soundcloud.Client(client_id=os.environ['SOUNDCLOUD_ID'])


def get_user_object(username):
    user_url = 'http://soundcloud.com/{}'.format(username)
    resolved_data = soundcloud_client.get('/resolve',
                                          url=user_url,
                                          allow_redirects=False)
    user_resource = soundcloud_client.get(resolved_data.obj['location'])

    return user_resource.obj


def download_track(track_url):
    resolved_data = soundcloud_client.get('/resolve',
                                          url=track_url, allow_redirects=False)

    track_data = soundcloud_client.get(resolved_data.url)
    track_title = track_data.obj['title']
    track_id = track_data.obj['id']

    soundcloud_stream_resource = track_data.obj['stream_url']
    stream_url = soundcloud_client.get(soundcloud_stream_resource,
                                       allow_redirects=False)

    # Create a legal filename.
    filename = "".join([c for c in track_title
                              if c.isalpha() or c.isdigit() or c==' ']).rstrip()

    with open('{} - {}.mp3'.format(filename, track_id), 'wb') as f:
        f.write(requests.get(stream_url.location).content)


def download_tracks(tracks):
    for track in tracks:
        print('Downloading: {}'.format(track.obj['title']))

        try:
            download_track(track.obj['permalink_url'])
        except:
            print('Problem downloading {}'.format(track.obj['title']))


def download_artist(username):
    user = get_user_object(username)
    user_tracks_resource = '/users/{}/tracks'.format(user['id'])
    user_tracks = soundcloud_client.get(user_tracks_resource)

    download_tracks(user_tracks)


def download_favorites(username):
    user = get_user_object(username)

    user_favorites_resource = '/users/{}/favorites'.format(user['id'])
    user_favorites = soundcloud_client.get(user_favorites_resource)

    download_tracks(user_favorites)


if __name__ == '__main__':
    if sys.argv[1] == 'track':
        download_track(sys.argv[1])
    elif sys.argv[1] == 'artist':
        download_artist(sys.argv[2])
    elif sys.argv[1] == 'favorites':
        download_favorites(sys.argv[2])

