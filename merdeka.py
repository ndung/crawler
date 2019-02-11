from dbconn import DBConn
from bs4 import BeautifulSoup, Comment
from datetime import timedelta, datetime
import requests
import re

class Merdeka:
    def crawl_content(self, url):
        result = []
        # find link page
        print url

        for i in range(1, 9):

            try:
                # find article link
                req = requests.get(url + '/index' + str(i) + '.html')
                print 'url:' + req.url
                soup = BeautifulSoup(req.text, "lxml")

                newsLink = soup.find('ul', {'class': 'mdk-idn-nd-centlist'}).find_all('li')
                print newsLink
                db = DBConn()

                # looping through article link
                for idx, news in enumerate(newsLink):

                    newsDict = {}
                    # print news

                    # find urll news
                    urlNews = "http://www.merdeka.com" + news.find('a').get('href')

                    print urlNews

                    if not urlNews.startswith('http://www.merdeka.com/foto'):

                        datestr = news.find('span', {'class': 'mdk-idn-date'}).string
                        date = self.formatDate(datestr)
                        print date

                        # find news content in url
                        reqNews = requests.get(urlNews)
                        soupNews = BeautifulSoup(reqNews.text, "lxml")
                        titleNews = soupNews.find('title').get_text()
                        print titleNews
                        keyword = soupNews.find('meta', {'name': 'keywords'}).get('content')
                        description = soupNews.find('meta', {'name': 'description'}).get('content')
                        section = soupNews.find('meta', {'property': 'section'}).get('content')

                        # find news content
                        newsContent = soupNews.find("div", {'class': 'mdk-body-paragpraph'})

                        if newsContent != None:
                            for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                                _ = elm.extract()
                            for elm in newsContent.find_all("div", {'id': 'section_terkait'}):
                                _ = elm.extract()
                            for elm in newsContent.find_all('a'):
                                del elm['href']
                                del elm['target']
                                del elm['rel']
                                del elm['title']
                            for elm in newsContent.find_all('img'):
                                _ = elm.extract()

                            newsContent['class'] = 'news'

                            content = newsContent.prettify().encode('utf-8').strip()

                            print content

                            # wrap in dictionary
                            newsDict['date'] = date
                            newsDict['url'] = urlNews
                            newsDict['title'] = titleNews
                            newsDict['content'] = content
                            newsDict['keyword'] = keyword
                            newsDict['description'] = description
                            newsDict['category'] = section
                            newsDict['source'] = 'merdeka'
                            result.append(newsDict)
                            db.save(newsDict)

            except Exception, err:
                print err
                pass

        return result

    def formatDate(self, date):
        a, b = date.split(',')
        d, m, y, w = b.strip().split(' ')
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
        return y + '-' + mm + '-' + d.rjust(2,'0') + ' ' + w

    def daterange(self, startDate, endDate):
        for n in range(int((endDate - startDate).days)):
            yield startDate + timedelta(n)

    def crawl(self, startDate, endDate):
        for single_date in self.daterange(startDate, endDate):
            datenews = str(single_date.strftime("%Y/%m/%d"))
            url = 'https://www.merdeka.com/indeks-berita/' + datenews
            self.crawl_content(url)