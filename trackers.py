import os
folder = os.path.dirname(__file__) + "/trackerslist"
excludes = [
    "blacklist.txt"
]
files = [x for x in os.listdir(folder) if x.endswith(".txt") and x not in excludes]

recommended = [
    "udp://tracker.opentrackr.org:1337/announce"
    "udp://p4p.arenabg.com:1337/announce",
    "udp://tracker.torrent.eu.org:451/announce",
    "udp://tracker.dler.org:6969/announce",
    "udp://open.stealth.si:80/announce",
    "udp://ipv4.tracker.harry.lu:80/announce",
    "https://opentracker.i2p.rocks:443/announce",

]

trackers = set()
for f in files:
    filepath = os.path.join(folder, f)
    with open(filepath, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines if line.strip()]
        for line in lines:
            if not line in trackers:
                trackers.add(line)

for t in recommended:
    if not t in trackers:
        trackers.add(t)


