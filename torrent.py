# from deluge_client import DelugeRPCClient
import time
from transmission_rpc import Client
from classes import Movie
import os
from dotenv import load_dotenv

load_dotenv()

# deluge_host="192.168.1.28"
# deluge_port=58846
# deluge_username="mbolivar"
# deluge_password="kkfvy"
# cleanup_path="/var/videos/films"

transmisison_host=os.getenv("TRANSMISSION_HOST")
transmisison_port=os.getenv("TRANSMISSION_PORT")
transmisison_username=os.getenv("TRANSMISSION_USERNAME")
transmisison_password=os.getenv("TRANSMISSION_PASSWORD")

def addMoviesTorrents(movies):
    client = Client(host=transmisison_host, port=transmisison_port, username=transmisison_username, password=transmisison_password)

    torrents_list = [h.hashString.lower() for h in client.get_torrents()]


    for movie in movies:
        filter_torrents = [t for t in movie.torrents if t.quality != "2160p"] #exclude super big files
        filter_torrents = sorted(filter_torrents, key=lambda x: (x.quality, x.size,-x.seeds )) #1080p comes first
        addedtorrent = False
        for torrent in filter_torrents:
            if addedtorrent:
                break
            if torrent.hash.lower() not in torrents_list:
                try:
                    client.add_torrent(torrent.getMagnetLink())
                    # client.core.add_torrent_magnet(torrent.getMagnetLink(), options)
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

