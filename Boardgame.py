
# coding: utf-8

# In[194]:

import urllib2, time, random, re
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import requests


# In[7]:

#find all the links given website and append to all_url list. From that list find all the links that end with /boardgame/somedigits
soup = BeautifulSoup(urllib2.urlopen(urllib2.Request("https://boardgamegeek.com/browse/boardgame")).read())
all_url = []
for i in range(1,6):
    print i
    soup = BeautifulSoup(urllib2.urlopen(urllib2.Request("https://boardgamegeek.com/browse/boardgame/page/" + str(i))).read())
    for a in soup.find_all('a', href = True):
        all_url.append(a['href'])
board_games = []
for url in all_url:
    if re.match('/boardgame/\d+\w+', url):
        board_games.append(url)


# In[236]:

#get the board game ID numbers
board_games_nums =[]
for b in board_games:
    d = re.search('\d+', b)
    board_games_nums.append(d.group(0))


# In[143]:

#find the descriptions of all the games and add to dictionary
games = list(set(board_games_nums))
dic ={}
while len(games)>0:
    print len(games)
    s = ','.join(games[:25])
    final_url = 'http://www.boardgamegeek.com/xmlapi/boardgame/' + s + '?comments=1'
    print final_url
    soup = BeautifulSoup(urllib2.urlopen(urllib2.Request(final_url)).read())
    for num in games[:25]:
        name_of_game = soup.find('boardgame', {'objectid': num}).find('name', {'primary' : 'true'}).text
        des = soup.find('boardgame', {'objectid': num}).description.text
        dic[name_of_game] = {}
        dic[name_of_game]['description'] = des
        #list_of_comments =[]
        #for c in soup.find('boardgame', {'objectid': num}).find_all('comment', {'usernames': True}):
        #    list_of_comments.append(c.text)
        #dic[name_of_game]['comments'] = ' '.join(list_of_comments)
    games = games[25:]

