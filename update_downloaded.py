#!/usr/bin/env python3

import sys
with open('/tmp/python_version.log', 'w') as f:
    f.write(sys.version)

exit()

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import Torrent  # Asegúrate de importar el modelo Torrent desde tu módulo
from configs import Config

config=Config()
# Ruta al archivo de la base de datos SQLite
db_path = config.sqlite_filename

# Crear una conexión a la base de datos
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)
session = Session()

# Obtener el ID del torrent desde los argumentos del script
torrent_id = sys.argv[1]  # Transmission pasará el ID del torrent como argumento

# Buscar el torrent por su ID
torrent = session.query(Torrent).filter_by(id=torrent_id).first()

if torrent:
    # Actualizar el campo 'downloaded' a True
    torrent.downloaded = True
    session.commit()
    print(f'Torrent {torrent_id} marcado como descargado.')
else:
    print(f'Torrent {torrent_id} no encontrado.')

# Cerrar la sesión
session.close()
