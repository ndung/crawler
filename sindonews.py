from dbconn import DBConn
from bs4 import BeautifulSoup, Comment
from datetime import timedelta, datetime
import requests
import re

class Sindonews:
    def crawl_content(self, datenews):
        result = []
        # find link page

        for i in range(0, 20):

            try:
                # find article link
                req = requests.get('https://index.sindonews.com/index/'+str(i)+'?t='+datenews)
                print 'url:'+req.url
                soup = BeautifulSoup(req.text, "lxml")

                newsLink = soup.find_all("div", {'class': 'indeks-title'})
                print newsLink
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

                    titleNews = soupNews.find('meta', {'name': 'title'}).get('content')
                    print titleNews
                    date = self.formatDate(soupNews.find('time').get_text())

                    if date is not None:
                        print date
                        keyword = ''
                        description = soupNews.find('meta', {'name': 'description'}).get('content')
                        category = ''

                        # find news content
                        newsContent = soupNews.find("div", {'id': 'content'})

                        if newsContent != None:

                            newsContent['class'] = 'news'
                            del newsContent['id']

                            for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                                _ = elm.extract()
                            for elm in newsContent.findAll("div", {"id": re.compile('div-gpt-ad.*')}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'image-content'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'baca-inline'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'class': 'baca-inline-head'}):
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

                            # wrap in dictionary
                            newsDict['date'] = date
                            newsDict['url'] = urlNews
                            newsDict['title'] = titleNews
                            newsDict['keyword'] = keyword
                            newsDict['description'] = description
                            newsDict['content'] = content
                            newsDict['source'] = 'sindonews'
                            newsDict['category'] = category
                            result.append(newsDict)
                            db.save(newsDict)
            except Exception, err:
                print err
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

    def daterange(self, startDate, endDate):
        for n in range(int ((endDate - startDate).days)):
            yield startDate + timedelta(n)

    def crawl(self, startDate, endDate):
        for single_date in self.daterange(startDate, endDate):
            datenews = str(single_date.strftime("%Y-%m-%d"))
            self.crawl_content(datenews)






