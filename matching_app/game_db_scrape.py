import urllib.request as req
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from time import sleep
from . import models
from django.db.utils import IntegrityError

def start_scrape():
    urls = ['https://www.gamer.ne.jp/game/PS5&sort=new']
    max_count = 0
    for i,url in enumerate(urls):
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        request = req.Request(url, headers=headers)
        res = req.urlopen(request)
        soup = BeautifulSoup(res, "html.parser")

        rows = soup.select('.gameTitleListBox')
        for j,row in enumerate(rows):
            #html 親要素
            images = row.find('div',attrs={"class": "image"})
            text = row.find('div',attrs={"class": "text"})

            #それぞれの要素をStringで抽出
            #ゲームタイトル
            game_name = text.find('p',attrs={"class": "title"}).find('a').text

            #ジャンル->list
            genre = text.find('div',attrs={"class": "tag"}).find_all('span',attrs={"class": "genre"})
            genre_list = [x.find('a').text for x in genre]

            #タグ->list
            tags = text.find('div',attrs={"class": "tag"}).find_all('span',attrs={"class": "theme"})
            tags_list = [x.find('a').text for x in tags]

            #プラットフォーム->list
            platform = text.find('div',attrs={"class": "tag"}).find_all('span',attrs={"class": "hard"})
            platform_list = [x.find('a').text for x in platform]
            
            game_obj = models.Game(game_name=game_name)
            
            #画像
            image = images.find('img').get('data-src')
            if not image == '/img/dummylogo.png':
                game_obj.image = 'images/sumgames_{}_{}.png'.format(i,j)
            
            #ゲーム説明
            detail = text.find('p',attrs={"class": "catchcopy"}).text
            if detail is not None:
                game_obj.detail = detail
            
            try:
                game_obj.save()
            except IntegrityError:
                continue
            
            if not image == '/img/dummylogo.png':
                try:
                    request = req.Request(urljoin('https://www.gamer.ne.jp',image), headers=headers)
                    with req.urlopen(request) as f:
                        data = f.read()
                        with open('./media/images/sumgames_{}_{}.png'.format(i,j), mode='wb') as local_file:
                            local_file.write(data)
                except HTTPError:
                    pass


            for g_name in genre_list:
                try:
                    genre_obj = models.Genre(genrename=g_name)
                    genre_obj.save()
                    game_obj.genre.add(genre_obj)
                except IntegrityError:
                    game_obj.genre.add(models.Genre.objects.get(genrename=g_name))
            
            for t_name in tags_list:
                try:
                    tags_obj = models.Tags(tag_name=t_name)
                    tags_obj.save()
                    game_obj.tags.add(tags_obj)
                except IntegrityError:
                    game_obj.tags.add(models.Tags.objects.get(tag_name=t_name))
            
            for p_name in platform_list:
                try:
                    platform_obj = models.Platform(platform_name=p_name)
                    platform_obj.save()
                    game_obj.platform.add(platform_obj)
                except IntegrityError:
                    game_obj.platform.add(models.Platform.objects.get(platform_name=p_name))


        next_page = soup.select_one('#gameList > div.mainContent > div.pager > ul > li.next > a')
        if next_page is not None:
            if url == 'https://www.gamer.ne.jp/game/PC&page=100&sort=new':
                urls.append("https://www.gamer.ne.jp/game/AC&sort=new")
            else:
                urls.append("https://www.gamer.ne.jp/game/" + next_page.get('href'))
        elif 'PS5' in url:
            urls.append("https://www.gamer.ne.jp/game/PS4&sort=new")
        elif 'PS4' in url:
            urls.append("https://www.gamer.ne.jp/game/PSVita&sort=new")
        elif 'PSVita' in url:
            urls.append("https://www.gamer.ne.jp/game/Switch&sort=new")
        elif 'Switch' in url:
            urls.append("https://www.gamer.ne.jp/game/XboxSX&sort=new")
        elif 'XboxSX' in url:
            urls.append("https://www.gamer.ne.jp/game/PC&sort=new")


        count = len(models.Game.objects.all())
        if url == 'https://www.gamer.ne.jp/game/AC&page=10':
            break
        print(count,url)
        sleep(1)