import requests
import json
from bs4 import BeautifulSoup
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
headers = {
        'user-agent': user_agent,
    }
source = requests.get('https://www.zillow.com/berkeley-ca/apartments/', headers = headers).text
soup = BeautifulSoup(source, 'lxml')
listings = soup.find_all('article', class_= 'list-card list-card-short list-card_not-saved list-card_building')
def filter_listings(listings, limit = 3000):
    addresses = []
    prices = []
    listings = [listing.text.split("|") for listing in listings]
    for i in range(len(listings)):
        listing = listings[i]
        if len(listings[i]) != 1:
            listing = listing[1]
        else:
            listing = listing[0]
        split_listing = listing.split("$")
        address = split_listing[0][:split_listing[0].find('CA') + 2].strip().replace(" ", '+')
        price = split_listing[1].split(" ")[0].strip('+').replace(",","")
        price = int(price)
        if price <= limit:
            addresses.append(address)
            prices.append(price)
    return addresses, prices
def find_distances(addresses, limit = 20):
    pairs = {}
    for address1 in addresses:
        for address2 in addresses:
            if address1 != address2 and (address1, address2) not in pairs and (address2, address1) not in pairs:
                origin = address1
                destination = address2
                mode = 'walking'
                response = requests.request('GET',f'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins={origin},DC&destinations={destination}&mode={mode}&key=AIzaSyDjHY05x8GSfh3qeNx6D1BNWXPVJ1UR4c0')
                response = response.content
                response = json.loads(response)
                time = response['rows'][0]['elements'][0]['duration']['text']
                if time.find('hour') == -1:
                    time = time.strip('mins')
                    time = int(time)
                    if time < limit:
                        address_pair = (address1, address2)
                        pairs[address_pair] = time
    return pairs
addresses, prices = filter_listings(listings)
print(find_distances(addresses, 5))
