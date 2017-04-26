
# coding: utf-8

# In[3]:

import urllib2, time, random, re
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd
import requests


# In[39]:

#find all the links given website and append to all_url list. From that list find all the links that end with /boardgame/somedigits
soup = BeautifulSoup(urllib2.urlopen(urllib2.Request("https://boardgamegeek.com/browse/boardgame")).read())
all_url = []
for i in range(1,6):
    soup = BeautifulSoup(urllib2.urlopen(urllib2.Request("https://boardgamegeek.com/browse/boardgame/page/" + str(i))).read())
    for a in soup.find_all('a', href = True):
        all_url.append(a['href'])
board_games = []
for url in all_url:
    if re.match('/boardgame/\d+\w+', url):
        board_games.append(url)


# In[94]:

board_games = list(set(board_games))
#get the board game ID numbers
board_games_and_nums =[]
nums_only =[]
for b in board_games:
    digits = re.search('\d+', b)
    last_digit_index = re.search('\d+', b).end()
    name_of_game = b[last_digit_index + 1:]
    board_games_and_nums.append([name_of_game, digits.group(0)])
    nums_only.append(digits.group(0))


# In[99]:

games = nums_only[:]
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
    games = games[25:]


# In[96]:

#get the top 5 forums and put in list for later processing later. group everything in dictionary
base_forum_list_url = 'https://www.boardgamegeek.com/xmlapi2/forumlist?id='
base_forum_url = 'https://www.boardgamegeek.com/xmlapi2/forum?id='
for number in board_games_and_nums:
    print 'num', number[1]
    final_forum_list_url = base_forum_list_url + number[1] + '&type=thing'
    forum_list = BeautifulSoup(urllib2.urlopen(urllib2.Request(final_forum_list_url)).read())
    ID = forum_list.find('forum', {'title': 'Reviews'}).get('id')
    final_forum_url = base_forum_url + ID + '&sort=hot'
    forum = BeautifulSoup(urllib2.urlopen(urllib2.Request(final_forum_url)).read())
    all_threads = forum.find_all('thread')
    list_of_top_five_threads = []
    for thread in all_threads[:5]:
        list_of_top_five_threads.append(thread.get('id'))
   
    words_in_top_five_threads = []
    thread_base_url = 'https://www.boardgamegeek.com/xmlapi2/thread?id='
    for thread_ID in list_of_top_five_threads:
        final_thread_url = thread_base_url + thread_ID 
        thread = BeautifulSoup(urllib2.urlopen(urllib2.Request(final_thread_url)).read())
        words_in_top_five_threads.append(thread.find('article').getText())
   
    dic[num[0]]['user_reviews'] = words_in_top_five_threads


# In[ ]:



