from dbconn import DBConn
from bs4 import BeautifulSoup, Comment
from datetime import timedelta, datetime
import requests
import re

class Suara:
    def crawl_content(self):
        result = []
        # find link page

        for i in range(1, 20):
            try:
                # find article link
                req = requests.get('https://www.suara.com/indeks/terkini/all/page--'+str(i))

                print req.url
                soup = BeautifulSoup(req.text, "lxml")

                newsLink = soup.find_all("div", {'class': 'item-content'})

                db = DBConn()

                # looping through article link
                for idx, news in enumerate(newsLink):
                    newsDict = {}
                    # print news

                    # find urll news
                    urlNews = news.find('a').get('href')
                    print urlNews

                    # find news content in url
                    reqNews = requests.get(urlNews)
                    soupNews = BeautifulSoup(reqNews.text, "lxml")

                    titleNews = soupNews.find('title').get_text().strip()
                    print titleNews
                    date = self.formatDate(soupNews.find('time', {'itemprop': 'datePublished'}).get_text().strip())
                    print date
                    keyword = soupNews.find('meta', {'name': 'news_keywords'}).get('content')
                    description = soupNews.find('meta', {'name': 'description'}).get('content')
                    category = ''
                    # find news content
                    newsContent = soupNews.find("div", {'class': 'content-article'})

                    newsContent = newsContent.find_all("div")[0]

                    # find paragraph in news content
                    if newsContent != None:
                        for elm in newsContent.findAll("div", {"class": re.compile('widget-ads.*')}):
                            _ = elm.extract()
                        for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                            _ = elm.extract()
                        for elm in newsContent.find_all('strong'):
                            temp = elm.get_text().lower().encode('utf-8')
                            if 'baca juga :' in temp or 'baca juga:' in temp:
                                _ = elm.extract()
                        for elm in newsContent.find_all('a'):
                            del elm['href']
                            del elm['target']
                            del elm['rel']
                            del elm['title']
                        for elm in newsContent.find_all('iframe'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('figure'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('img'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('script'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('div'):
                            temp = elm.get_text().lower().encode('utf-8').strip()
                            if temp == '':
                                _ = elm.extract()

                        newsContent['class'] = 'news'

                        content = newsContent.prettify().encode('utf-8').strip()

                        print content

                        # wrap in dictionary
                        newsDict['date'] = date
                        newsDict['url'] = urlNews
                        newsDict['title'] = titleNews
                        newsDict['keyword'] = keyword
                        newsDict['description'] = description
                        newsDict['content'] = content
                        newsDict['category'] = category
                        newsDict['source'] = 'suara'
                        result.append(newsDict)
                        db.save(newsDict)
            except Exception as e:
                print e
                pass

        return result

    def formatDate(self, date):
        try:
            a, b = date.split(',')
            d, m, y, _, w, wib = b.strip().split(' ')
            if m.lower() == 'januari':
                mm = '01'
            elif m.lower() == 'februari':
                mm = '02'
            elif m.lower() == 'maret':
                mm = '03'
            elif m.lower() == 'april':
                mm = '04'
            elif m.lower() == 'mei':
                mm = '05'
            elif m.lower() == 'juni':
                mm = '06'
            elif m.lower() == 'juli':
                mm = '07'
            elif m.lower() == 'agustus':
                mm = '08'
            elif m.lower() == 'september':
                mm = '09'
            elif m.lower() == 'oktober':
                mm = '10'
            elif m.lower() == 'november':
                mm = '11'
            elif m.lower() == 'desember':
                mm = '12'
            return y + '-' + mm + '-' + d.rjust(2,'0') + ' ' + w + ':00'
        except Exception, err:
            print err
            pass
        return None

    def crawl(self):
        self.crawl_content()





