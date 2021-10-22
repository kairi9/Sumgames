import urllib.request as req
from bs4 import BeautifulSoup
from time import sleep

urls = ['https://www.gamer.ne.jp/game/&sort=new']

for url in urls:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }
    request = req.Request(url, headers=headers)
    res = req.urlopen(request)
    soup = BeautifulSoup(res, "html.parser")

    rows = soup.select('.gameTitleListBox')
    for row in rows:
        images = row.find('div',attrs={"class": "image"})
        text = row.find('div',attrs={"class": "text"})

        game_name = text.find('p',attrs={"class": "title"}).find('a').text
        genre = text.find('div',attrs={"class": "tag"}).find_all('span',attrs={"class": "genre"})
        genre_list = [x.find('a').text for x in genre]
        #image = 
        tags = text.find('div',attrs={"class": "tag"}).find_all('span',attrs={"class": "theme"})
        tags_list = [x.find('a').text for x in tags]
        platform = text.find('div',attrs={"class": "tag"}).find_all('span',attrs={"class": "hard"})
        platform_list = [x.find('a').text for x in platform]
        
        


    next_page = soup.select_one('#gameList > div.mainContent > div.pager > ul > li.next > a')
    if next_page is not None:
        urls.append("https://www.gamer.ne.jp/game/" + next_page.get('href'))
    
    sleep(1)