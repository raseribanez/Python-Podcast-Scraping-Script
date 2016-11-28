# A modification of Michael Kennedy's original script for scraping episodes
# This version is aimed at the rss episodes link (all 80 podcasts)
# All I changed is the url in line 11
# Runs in Python 3 | Needs requests package | mp3s are 4.4GB in total

import requests
import sys
from xml.etree import ElementTree

def main():
    rss_url = 'https://talkpython.fm/episodes/rss' # Edited this link for all episodes

    resp = requests.get(rss_url)
    if resp.status_code != 200:
        print("ERROR: {}".format(resp.status_code))
        return

    xml_text = resp.text
    xml = ElementTree.fromstring(xml_text)
    
    items = xml.findall('channel/item')
    print("Downloading {} episodes...".format(len(items)))
    for item in items:
        url = item.find('enclosure').attrib.get('url')
        title = item.find('title').text
        print(title + " ... ", end='')
        sys.stdout.flush()
        print(url)
        name = url.split('/')[-1]
        resp = requests.get(url, stream=True)
        with open(name, 'wb') as fout:
            for chunk in resp.iter_content(1024*32):
                fout.write(chunk)
        print("done.")


if __name__ == '__main__':
    main()
