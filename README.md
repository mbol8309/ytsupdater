# Introduction
This is a script to download torrent data automatically from yts.mx and store in local db. Later with that info and with selected filters download torrent with transmission-gtk to jellyfin folder
# Requirements
- [transmission-daemon](https://wiki.debian.org/es/BitTorrent/Transmission-daemon)
- [jellyfin](https://jellyfin.org)
# Usage
## Create .env
Create a file .env with transmission connect info. An example can be seen in `.env.example`
## Install dependencies
I think this file is ok, but if some error, please comment
`pip install -r requirements`
## Run
`python start.py`
  
