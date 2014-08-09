#!/usr/bin/env python
# -*- coding: utf-8 -*

import os
import platform
import sqlite3
from glob import glob
from urllib2 import urlopen

HOME_DIR = os.path.expanduser('~')
BACKUP_DIR = os.path.join(HOME_DIR, 'FramapadBackup')

def get_profiles(os_type):

    if os_type == "Linux":
            firefox_profiles = glob(HOME_DIR + "/.mozilla/firefox/*.default/")
            chrome_profiles = glob(HOME_DIR + "/.config/google-chrome/Default/")
            chromium_profiles = glob(HOME_DIR + "/.config/chromium/Default/")

    elif os_type == "Windows":
        firefox_profiles = glob(os.getenv('APPDATA') + "\Mozilla\Firefox\Profiles\*.default\\")

        if platform.release() == "XP":
            chrome_profiles = glob("C:\Documents and Settings\{}\Local Settings\Application Data\Google\Chrome\User Data\Default\\".format(os.getenv("USERNAME")))
            chromium_profiles = glob("C:\Documents and Settings\{}\Local Settings\Application Data\Chromium\User Data\Default\\".format(os.getenv("USERNAME")))
        else:
            chrome_profiles = glob("C:\Users\{}\AppData\Local\Google\Chrome\User Data\Default\\".format(os.getenv("USERNAME")))
            chromium_profiles = glob("C:\Users\{}\AppData\Local\Chromium\User Data\Default\\".format(os.getenv("USERNAME")))
    else:
        firefox_profiles = glob(HOME_DIR + "/Library/Mozilla/.mozilla/firefox/*.default/")
        chrome_profiles = glob(HOME_DIR + "/Library/Application Support/Google/Chrome/Default/")
        chromium_profiles = glob(HOME_DIR + "/Library/Application Support/Chromium/Default/")

    return firefox_profiles, chrome_profiles, chromium_profiles

def retrieve_firefox_urls(profile):
    conn = sqlite3.connect(profile + 'places.sqlite')

    urls = conn.execute('''SELECT DISTINCT url
                            FROM moz_places
                            WHERE url
                            LIKE "%lite%framapad.org/p/%"
                            AND url NOT LIKE "%/timeslider%"
                            AND url NOT LIKE "%/";''')

    return urls

def retrieve_chrome_urls(profile):
    conn = sqlite3.connect(profile + 'History')

    urls = conn.execute('''SELECT DISTINCT url
                            FROM urls
                            WHERE url
                            LIKE "%lite%framapad.org/p/%"
                            AND url NOT LIKE "%/timeslider%"
                            AND url NOT LIKE "%/";''')

    return urls

def save_text(url):
    path = BACKUP_DIR + url.split('/')[-1] + ".txt"

    if not os.path.exists(path):
        content = urlopen(url + '/export/txt')

        with open(path, 'w') as f:
            f.write(content.read())


if __name__ == "__main__":

    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)

    firefox_profiles, chrome_profiles, chromium_profiles = get_profiles(platform.system())

    urls = []

    for profile in firefox_profiles:
        urls += retrieve_firefox_urls(profile)

    for profile in chrome_profiles + chromium_profiles:
        urls += retrieve_chrome_urls(profile)

    for url in urls:
        print("Téléchargement de {}".format(url[0]))
        save_text(url[0])

    print("Tous les pads trouvés ont été téléchargés ici : {}".format(BACKUP_DIR))

