import sys
import os

import requests
import soundcloud


def download_track(track_url):
    soundcloud_client = soundcloud.Client(client_id=os.environ['SOUNDCLOUD_ID'])
    resolved_data = soundcloud_client.get('/resolve', url=track_url, allow_redirects=False)

    track_data = soundcloud_client.get(resolved_data.url)
    track_title = track_data.obj['title']
    track_id = track_data.obj['id']

    soundcloud_stream_resource = track_data.obj['stream_url']
    stream_url = soundcloud_client.get(soundcloud_stream_resource, allow_redirects=False)

    with open('{} - {}.mp3'.format(track_title, track_id), 'wb') as f:
        f.write(requests.get(stream_url.location).content)

if __name__ == '__main__':
    print(sys.argv[1])
    download_track(sys.argv[1])
