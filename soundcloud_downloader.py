import sys
import os

import requests
import soundcloud


soundcloud_client = soundcloud.Client(client_id=os.environ['SOUNDCLOUD_ID'])


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


def download_artist(username):
    artist_url = 'http://soundcloud.com/{}'.format(username)
    resolved_data = soundcloud_client.get('/resolve',
                                          url=artist_url,
                                          allow_redirects=False)

    user_resource = soundcloud_client.get(resolved_data.obj['location'])
    user_tracks_resource = '/users/{}/tracks'.format(user_resource.obj['id'])
    user_tracks = soundcloud_client.get(user_tracks_resource)

    for track in user_tracks:
        print('Downloading: {}'.format(track.obj['title']))

        try:
            download_track(track.obj['permalink_url'])
        except:
            print('Problem downloading {}'.format(track.obj['title']))


if __name__ == '__main__':
    if sys.argv[1] == 'track':
        download_track(sys.argv[1])
    elif sys.argv[1] == 'artist':
        download_artist(sys.argv[2])

