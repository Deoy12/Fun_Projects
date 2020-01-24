from bs4 import BeautifulSoup
import requests


source = requests.get(f'https://caldining.berkeley.edu/menu.php').text
soup = BeautifulSoup(source, 'lxml')
directory = {}
for meals in soup.find_all('div', class_="desc_wrap_ck3"):
    location, meal = [x.text for x in meals.find_all('h3')]
    item_list = []
    for item in meals.find_all('p'):
        item_list.append(item.text)
    dict_key = location + "/" + meal
    directory[dict_key.replace(" ", "")] = item_list
print(directory['Foothill/Dinner'])
 

   
   
   
