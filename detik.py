from dbconn import DBConn
from bs4 import BeautifulSoup, Comment
from datetime import timedelta, datetime
import requests
import re

class Detik:
    def crawl_content(self, datenews):
        result = []
        # find link page

        for i in range(1, 20):
            try:
                # find article link
                req = requests.get('https://news.detik.com/indeks/all/'+str(i)+'?date='+datenews.replace("-","%2F"))

                print req.url
                soup = BeautifulSoup(req.text, "lxml")
                newsLink = soup.find_all("div", {'class': 'desc_idx ml10'})

                db = DBConn()

                # looping through article link
                for idx, news in enumerate(newsLink):
                    newsDict = {}
                    # print news

                    # find urll news
                    urlNews = news.find('a').get('href')
                    print urlNews

                    if not urlNews.startswith('https://news.detik.com/detiktv') and not urlNews.startswith('https://news.detik.com/infografis') and not urlNews.startswith('https://news.detik.com/foto-news'):
                        # find news content in url
                        reqNews = requests.get(urlNews)
                        soupNews = BeautifulSoup(reqNews.text, "lxml")

                        titleNews = soupNews.find('title').get_text()
                        print titleNews
                        date = soupNews.find('meta', {'name': 'publishdate'}).get('content').replace('/', '-')
                        keyword = soupNews.find('meta', {'name': 'keywords'}).get('content')
                        description = soupNews.find('meta', {'name': 'description'}).get('content')

                        # find news content
                        newsContent = soupNews.find("div", {'class': 'detail_text'})

                        # find paragraph in news content
                        if newsContent!=None :
                            for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                                _ = elm.extract()
                            for elm in newsContent.findAll("div", {"id": re.compile('div-gpt-ad.*')}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'foto_story'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'lihatjg'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'clearfix mb20'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'detail_tag'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'news_tag'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'adL'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'adm'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'pic_artikel'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("table", {'class': 'linksisip'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("table", {'class': 'pic_artikel_sisip_table'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all('strong'):
                                temp = elm.get_text().lower().encode('utf-8')
                                if temp.startswith('simak juga') or temp.startswith('tonton juga'):
                                    _ = elm.extract()
                            for elm in newsContent.find_all("a", {'class': 'embed'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all('a'):
                                del elm['href']
                                del elm['rel']
                                del elm['target']
                                del elm['title']
                            for elm in newsContent.find_all('img'):
                                _ = elm.extract()
                            for elm in newsContent.find_all('script'):
                                _ = elm.extract()
                            for elm in newsContent.find_all('div'):
                                temp = elm.get_text().lower().encode('utf-8').strip()
                                if temp == '':
                                    _ = elm.extract()

                            newsContent['class'] = 'news'
                            del newsContent['id']

                            content = newsContent.prettify().encode('utf-8').strip()

                            print content

                            # wrap in dictionary
                            newsDict['date'] = date
                            newsDict['url'] = urlNews
                            newsDict['title'] = titleNews
                            newsDict['keyword'] = keyword
                            newsDict['description'] = description
                            newsDict['content'] = content
                            newsDict['category'] = 'news'
                            newsDict['source'] = 'detik'
                            result.append(newsDict)
                            db.save(newsDict)
            except Exception as e:
                print e
                pass

        return result

    def daterange(self, startDate, endDate):
        for n in range(int ((endDate - startDate).days)):
            yield startDate + timedelta(n)

    def crawl(self, startDate, endDate):
        for single_date in self.daterange(startDate, endDate):
            datenews = str(single_date.strftime("%m-%d-%Y"))
            self.crawl_content(datenews)





