#
# ncPirate
# displays Pirate Bay search results in a terminal interface
# Uses Tinycurses?
# David Bergeron
#

import sys, requests, re
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

        torrent_list = build_list(target)
        display_top( torrent_list, 4)

    except:
        sys.exit()
    



