# from deluge_client import DelugeRPCClient
import time
from transmission_rpc import Client
from classes import Movie
import os
from dotenv import load_dotenv
from configs import Config
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
download_dir=os.getenv("DOWNLOAD_DIR")
config = Config()

def get_free_space(path):
    """Devuelve el espacio libre disponible en bytes en el directorio especificado."""
    statvfs = os.statvfs(path)
    return statvfs.f_frsize * statvfs.f_bavail

def get_directory_size(path):
    """Devuelve el tamaño total del directorio en bytes."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def addMoviesTorrents(movies):
    client = Client(host=config.transmisison_host, port=config.transmisison_port, username=config.transmisison_username, password=config.transmisison_password)

    torrents_list = [h.hashString.lower() for h in client.get_torrents()]
    download_dir = config.download_dir
    current_size = get_directory_size(download_dir)
    max_download_size = int(config.max_download_size)
    print(f"Tamaño actual del directorio '{download_dir}': {current_size / (1024 ** 3):.2f} GB")
    print(f"Tamaño máximo permitido para descargas: {max_download_size / (1024 ** 3):.2f} GB")


    for movie in movies:
        filter_torrents = [t for t in movie.torrents if t.quality != "2160p"] #exclude super big files
        filter_torrents = sorted(filter_torrents, key=lambda x: (x.quality, x.size,-x.seeds )) #1080p comes first
        addedtorrent = False
        
        for torrent in filter_torrents:
            torrent_size = torrent.size_bytes
            if addedtorrent:
                break
            if torrent.hash.lower() not in torrents_list:
                if current_size + torrent_size <= max_download_size:
                    try:
                        client.add_torrent(torrent.getMagnetLink(), download_dir=download_dir)
                        # client.core.add_torrent_magnet(torrent.getMagnetLink(), options)
                        addedtorrent = True
                        current_size += torrent_size
                        print(f"Added film {movie.title}.")
                        if movie != movies[-1]:
                            print("Waiting few seconds to add more")
                            for i in range(15):
                                print(".", end='', flush=True)
                                time.sleep(1)
                            print('\nGoing for more')
                    except Exception as e:
                        print('Some error adding this torrent goin for more')
                else:
                    print(f"No hay suficiente espacio para descargar '{movie.title}'")
                    break
            else:
                addedtorrent = True
def cleanTorrents():
    client = Client(host=config.transmisison_host, port=config.transmisison_port, username=config.transmisison_username, password=config.transmisison_password)
    torrents_list = client.get_torrents()
    for torrent in torrents_list:
        if torrent.status == "seeding":
            print(f"Removing torrent {torrent.name}")
            client.remove_torrent(torrent.id, delete_data=False)
            print(f"Torrent {torrent.name} removed")
            print(f"Waiting 5 seconds to prevent block")
            time.sleep(5)
