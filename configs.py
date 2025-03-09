import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    _instance = None  # Atributo de clase para almacenar la instancia única

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            # Inicialización de las configuraciones
            cls._instance.transmisison_host=os.getenv("TRANSMISSION_HOST","localhost")
            cls._instance.transmisison_port=os.getenv("TRANSMISSION_PORT","9091")
            cls._instance.transmisison_username=os.getenv("TRANSMISSION_USERNAME","transmission")
            cls._instance.transmisison_password=os.getenv("TRANSMISSION_PASSWORD","transmission")
            cls._instance.download_dir=os.getenv("DOWNLOAD_DIR","./downloads")
            cls._instance.film_year=os.getenv("FILM_YEAR",2025)
            cls._instance.sqlite_filename=os.getenv("SQLITE_FILENAME","movies.sqlite")
            cls._instance.yts_url=os.getenv("YTS_URL","https://yts.mx")
            cls._instance.minimun_rating=os.getenv("MINIMUM_RATING",7)
            cls._instance.max_download_size=os.getenv("MAX_DOWNLOAD_SIZE",7)
            cls._instance.start_page=os.getenv("START_PAGE",1)
        return cls._instance
    