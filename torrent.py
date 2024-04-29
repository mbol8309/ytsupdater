from deluge_client import DelugeRPCClient
import os, shutil
from dbFilter import movies
import time
import tempfile
import requests

deluge_host="192.168.1.28"
deluge_port=58846
deluge_username="mbolivar"
deluge_password="kkfvy"
cleanup_path="/var/videos/films"

client = DelugeRPCClient(deluge_host, deluge_port, deluge_username, deluge_password)
client.connect()

options= {
    "move_completed": True,
    "move_completed_path": "/var/videos/films",
    "stop_at_ratio": True,
    "stop_ration": 2,
    "auto_managed": True,
    "max_upload_slots": 1,
    "max_upload_speed": 20
}

torrents_list = client.core.get_torrents_status({}, ['name', 'download_location'])
tmp_folder = tempfile.mkdtemp()

for movie in movies:
    filter_torrents = [t for t in movie.torrents if t.quality != "2160p"] #exclude super big files
    filter_torrents = sorted(filter_torrents, key=lambda x: (x.quality, x.size,-x.seeds )) #1080p comes first
    addedtorrent = False
    for torrent in filter_torrents:
        if addedtorrent:
            break
        hash_bytes = torrent.hash.lower().encode('utf-8')
        if hash_bytes not in torrents_list:
            try:
                client.core.add_torrent_magnet(torrent.getMagnetLink(), options)
                addedtorrent = True
                print(f"Added film {movie.title}. Waiting few seconds to add more")
                for i in range(15):
                    print(".", end='', flush=True)
                    time.sleep(1)
                print('\nGoing for more')
            except Exception as e:
                print('Some error adding this torrent goin for more')
        else:
            addedtorrent = True

