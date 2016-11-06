# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 12:43:02 2016
CIAN parser
"""

import requests # библиотека для создания собственных запросов к серверам
import re    # регулярные выражения
from bs4 import BeautifulSoup    # для обработки веб страниц
import pandas as pd    # работа с таблицами
import time
import math #for distance betwen two points

#%% delete html tegs
def html_stripper(text):
    return re.sub('<[^<]+?>', '', str(text))
    
#%% link to page with flats. p=n has to be substituted
district = 'http://www.cian.ru/cat.php?deal_type=sale&district%5B0%5D=13&district%5B1%5D=14&district%5B2%5D=15&district%5B3%5D=16&district%5B4%5D=17&district%5B5%5D=18&district%5B6%5D=19&district%5B7%5D=20&district%5B8%5D=21&district%5B9%5D=22&engine_version=2&offer_type=flat&p={}&room1=1&room2=1&room3=1&room4=1&room5=1&room6=1'

# donwload links to all flats
links = []
for page in range(1, 30):
    page_url = district.format(page) #prepare link to page
    
    
    search_page = requests.get(page_url) #download page
    search_page = search_page.content
    search_page = BeautifulSoup(search_page, 'lxml') # parce page
    
    flat_urls = search_page.findAll('div', attrs = {'ng-class':"{'serp-item_removed': offer.remove.state, 'serp-item_popup-opened': isPopupOpen}"})
    flat_urls = re.split('http://www.cian.ru/sale/flat/|/" ng-class="', str(flat_urls)) #split to separate links
    
    for link in flat_urls:
        if link.isdigit():
            links.append(link)

flatStats = {} #dictionary to write stats of a flat
           
# url to flat is flat_url = 'http://www.cian.ru/sale/flat/' + links[i] + '/'
#%% get price
def getPrice(flat_page):
    price = flat_page.find('div', attrs={'id':'price_rur', 'style':'display: none;visibility: hidden;'})
    price = html_stripper(price)
    price = price.replace(',', '.')
    flatStats['Price']  = int(float(price))

#%% get information from table     
def getTableInformation(flat_page):
    table = flat_page.find('table', attrs={'class':'object_descr_props flat sale', 'style':'float:left'})
    table = html_stripper(table)
    
    # answers are written to flatStats
    
    # floor and number of floors
    floors = (re.split('Этаж:\n\n|Тип дома', table)[1])
    floors = re.findall('(\d+)', floors)
    flatStats['Floor'] = int(floors[0])
    #sometimes there is no information, so
    try:
        flatStats['Nfloors'] = int(floors[1])
    except IndexError:
        flatStats['Nfloors'] = 'NA'
    
    # space
    Totsp  = re.split('Общая площадь:\n\n|\xa0м2', table)[1]
    Totsp = Totsp.replace(',', '.')
    if re.search(r'(–|-)', Totsp): flatStats['Totsp'] = 'NA'
    else:
        flatStats['Totsp'] = float(Totsp)
    
    Livesp = re.split('Жилая площадь:\n\n|\xa0м2\n\n\n\nПлощадь кухни:', table)[1]
    Livesp = Livesp.replace(',', '.')
    if re.search(r'(–|-)', Livesp): flatStats['Livesp'] = 'NA'
    else:
        flatStats['Livesp'] = float(Livesp)
    
    # kitchen
    Kitsp = re.split('Площадь кухни:\n\n|\n\n\nСовмещенных санузлов:', table)[1]
    Kitsp = Kitsp.replace(',', '.')
    if re.search(r'(–|-)', Kitsp): flatStats['Kitsp'] = 'NA'
    else:
        Kitsp = re.findall('(\d+.\d+|\d+)', Kitsp)[0]
        flatStats['Kitsp'] = float(Kitsp)
    
    # phone
    if re.search('Телефон', table):
        Tel = re.split('Телефон:\n|\n\n\nВид из окна:', table)[1]
        if re.search(r'(нет|–|-)', Tel): flatStats['Tel'] = 0
        else: flatStats['Tel'] = 1
    else: flatStats['Tel'] = 'NA'
        
    # balcony
    Bal = re.split('Балкон:\n|\n\n\nЛифт:', table)[1]
    if re.search(r'(нет|–|-)', Bal): flatStats['Bal'] = 0
    else: flatStats['Bal']=1
        
    # house type
    Type = (re.split('Тип дома:\n\n|\n\n\nТип продажи:', table)[1])
    if re.search(r'(монолит|кирпич|жб|желез)', Type): flatStats['Brick']=1
    else: flatStats['Brick']=0

    if re.search('новостр', Type): flatStats['New']=1
    else: flatStats['New']=0

#%% get coordinates
def getCoords(flat_page):
    coords = flat_page.find('div', attrs={'class':'map_info_button_extend'}).contents[1]
    coords = re.findall(r'\d+\.\d+', str(coords) )
    lat, lon = float(coords[0]), float(coords[1])
    Mlat, Mlon = 55.753709,  37.619813
    dist = math.sqrt( (Mlat-lat)**2 + (Mlon-lon)**2 ) # still can not find information how to convert this to km
    flatStats['lat'], flatStats['lon'], flatStats['Dist'] = lat, lon, dist

#%% room numbers
def getRoom(flat_page):
    rooms = flat_page.find('div', attrs={'class':'object_descr_title'})
    rooms = html_stripper(rooms)
    try:
        rooms = re.findall(r'\d+-комн', rooms)[0] #sometimes there are 10+ rooms, so d+
        rooms = re.findall(r'\d+', rooms)[0]
        flatStats['Rooms'] = int(rooms)
    except:
        flatStats['Rooms'] = 'NA'


#%% metro 
def getMetro(flat_page):
    try:
        metro = flat_page.find('a', attrs={'class':'object_item_metro_name', 'target':'_blank', 'rel':'nofollow'})
        metro = metro.contents[0]
    
        metrdist = flat_page.find('span', attrs={'class':'object_item_metro_comment'}).contents[0]
        Metrdist = int(re.findall(r'\d+', metrdist)[0])
        if re.search('пешком', metrdist): Walk = 1 #may be there are another key words, but I can not find
        else: Walk = 0
    except:
        Walk, Metrdist = 'NA', 'NA'
        
    flatStats['Metrdist'] = Metrdist
    flatStats['Walk'] = Walk
#%% cycle for all flats
#FlatsData = pd.DataFrame({'District', 'Rooms', 'Price', 'Totsp', 'Livesp', 'Kitsp', 'Dist', 'Metrdist', 'Walk', 'Brick', 'Tel', 'Bal', 'Floor', 'Nfloors', 'New'})
FlatsData = pd.DataFrame()
for i in range(len(links)):
#for i in range(600,650): #test cycle
    flat_url = 'http://www.cian.ru/sale/flat/' + links[i] + '/'
    flat_page = requests.get(flat_url)
    flat_page = flat_page.content
    flat_page = BeautifulSoup(flat_page, 'lxml')
    
 #   flatStats['District']=i # if there are another districts
    getPrice(flat_page)
    getCoords(flat_page)
    getRoom(flat_page)
    getMetro(flat_page)
    getTableInformation(flat_page)
    
    FlatsData = FlatsData.append(flatStats, ignore_index=True)
    
    if not i%50:
        print('parcing flat no {}'.format(i) ) #controle the progress
    
    
#%% write answer to file
FlatsData.to_csv('flats_CAD.csv', index=True)
    
    