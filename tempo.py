from bs4 import BeautifulSoup, Comment
from datetime import timedelta, datetime
import requests
from dbconn import DBConn
import re

class Tempo:

    def crawl_content(self, url):
        result = []

        try:
            # find article link
            req = requests.get(url)
            print req.url
            soup = BeautifulSoup(req.text, "lxml")
            newsLink = soup.find_all("div", {'class': 'card card-type-1'})

            db = DBConn()

            # looping through article link
            for idx, news in enumerate(newsLink):
                newsDict = {}

                # find urll news
                urlNews = news.find('a').get('href')
                print urlNews

                # find news content in url
                reqNews = requests.get(urlNews)
                soupNews = BeautifulSoup(reqNews.text, "lxml")

                titleNews = soupNews.find('title').get_text()
                print titleNews
                datestr = soupNews.find('meta', {'property': 'article:published_time'}).get('content').replace('T',' ')
                date = datestr[0:19]
                print date
                keyword = soupNews.find('meta', {'name': 'keywords'}).get('content')
                description = soupNews.find('meta', {'name': 'description'}).get('content')

                section = soupNews.find('meta', {'property': 'article:section'}).get('content')

                # find news content
                newsContent = soupNews.find("div", {'id': 'isi'})

                # find paragraph in news content
                if newsContent != None:

                    newsContent['class'] = 'news'
                    del newsContent['id']
                    del newsContent['itemprop']

                    for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                        _ = elm.extract()
                    for elm in newsContent.findAll("div", {"id": "inarticle"}):
                        _ = elm.extract()
                    for elm in newsContent.findAll("div", {"class": "paging"}):
                        _ = elm.extract()
                    for elm in newsContent.find_all('p'):
                        temp = elm.get_text().lower().encode('utf-8')
                        if 'baca:' in temp or 'baca juga:' in temp :
                            _ = elm.extract()
                    for elm in newsContent.find_all('div'):
                        temp = elm.get_text().lower().encode('utf-8').strip()
                        if temp=='' or 'baca juga:' in temp :
                            _ = elm.extract()
                    for elm in newsContent.find_all('strong'):
                        temp = elm.get_text().lower().encode('utf-8')
                        if 'baca:' in temp or 'baca :' in temp:
                            _ = elm.extract()
                    for elm in newsContent.find_all('script'):
                        _ = elm.extract()
                    for elm in newsContent.find_all('a'):
                        del elm['href']
                        del elm['rel']
                        del elm['target']
                        del elm['title']
                    for elm in newsContent.find_all('img'):
                        _ = elm.extract()

                    content = newsContent.prettify().encode('utf-8').strip()

                    print content

                    # wrap in dictionary
                    newsDict['date'] = date
                    newsDict['url'] = urlNews
                    newsDict['title'] = titleNews
                    newsDict['keyword'] = keyword
                    newsDict['description'] = description
                    newsDict['content'] = content
                    newsDict['category'] = section
                    newsDict['source'] = 'tempo'

                    db.save(newsDict)
                    result.append(newsDict)

        except Exception as e:
            print e

        return result

    def daterange(self, startDate, endDate):
        for n in range(int ((endDate - startDate).days)):
            yield startDate + timedelta(n)

    def crawl(self, startDate, endDate):
        for single_date in self.daterange(startDate, endDate):
            datenews = str(single_date.strftime("%Y/%m/%d"))
            url = 'https://www.tempo.co/indeks/' + datenews
            self.crawl_content(url)



