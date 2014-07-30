#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import platform
import sqlite3
from glob import glob
from urllib2 import urlopen

OS_TYPE = platform.system()
HOME_DIR = os.getenv('HOME')
BACKUP_DIR = HOME_DIR + '/FramapadBackup/'

def retrieve_urls(profile):
    conn = sqlite3.connect(profile + 'places.sqlite')

    urls = conn.execute('''SELECT DISTINCT url
                            FROM moz_places
                            WHERE url
                            LIKE "%lite%framapad.org/p/%"
                            AND url NOT LIKE "%/timeslider%"
                            AND url NOT LIKE "%/";''')

    return urls

def save_text(url):
    content = urlopen(url + '/export/txt')
    path = BACKUP_DIR + url.split('/')[-1]

    with open(path + '.txt', 'w') as f:
        f.write(content.read())


if __name__ == "__main__":

    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)

    if OS_TYPE == "Linux":
        profiles = glob(HOME_DIR + "/.mozilla/firefox/*.default/")
    elif OS_TYPE == "Windows":
        profiles = glob(os.getenv('APPDATA') + "\Mozilla\Firefox\Profiles\*.default\\")
    else:
        profiles = glob(HOME_DIR + "/Library/Mozilla/.mozilla/firefox/*.default/")

    for profile in profiles:
        urls = retrieve_urls(profile)

        for url in urls:
            print("Téléchargement de {}".format(url[0]))
            save_text(url[0])

    print("Tous les pads trouvés ont été téléchargés ici : {}".format(BACKUP_DIR))

