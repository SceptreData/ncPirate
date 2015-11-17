#
# ncPirate script
# Displays Pirate Bay search results in a terminal interface
# David Bergeron

import sys, requests, re, os
from bs4 import BeautifulSoup
    
def pSearch( target ):
    
    results = []

    target = requests.utils.quote(target)
    url = 'https://thepiratebay.la/search/{0}/0/99/0'.format(target)
    soup = BeautifulSoup(requests.get(url).content, "lxml")

    for listing in soup.select("table#searchResult > tr"):
        seeds = int(listing.findChildren()[15].text)
        if seeds == 0:
            continue
        title = listing.find('a', {'class': 'detLink'}).text
        url = str(listing.find('a', href = re.compile('magnet'))).split('"')[1]
        
        results.append( ( seeds, title,  url ) )

    results.sort(reverse = True)

    return results

def open_magnet( magnet ):
    
    xdg_string = '/usr/bin/xdg-open'
    target = ' '.join((xdg_string, magnet.split('&amp')[0]))
    print(target)
    os.system(target)
    
def display_top( torrent_list, n):
    for i in range(n):
        print(torrent_list[i][0], torrent_list[i][1])
    
if __name__ == '__main__':
    try:
        print("Welcome to ncPirate")
        if len(sys.argv) > 1:
            target = sys.argv[1]
        else:
            target = input('Enter Seach Query -> ')

        results = pSearch(target)
        display_top( results , 4)
        download_index = int(input("Select torrent to download (0-4)"))
        open_magnet( results[download_index][2])

    except:
        sys.exit()
    
