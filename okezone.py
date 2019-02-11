from dbconn import DBConn
from bs4 import BeautifulSoup, Comment
import re
import requests

class Okezone:
    def crawl_content(self):
        result = []
        # find link page
        url = 'https://index.okezone.com/home/index/'

        for i in range(0, 9):

            try:
                # find article link
                req = requests.get(url+str(i*15))
                print 'url:'+req.url
                soup = BeautifulSoup(req.text, "lxml")

                newsLink = soup.find_all("div", {'class': 'content-hardnews pad-index'})
                print newsLink
                db = DBConn()

                # looping through article link
                for idx, news in enumerate(newsLink):

                    newsDict = {}

                    a,b = news.get_text().strip().split('|')
                    c,d = b.strip().split('WIB')
                    e,f = c.strip().split(',')

                    datestr = f.strip()

                    # find urll news
                    urlNews = news.find('a').get('href')
                    print urlNews

                    date = self.formatDate(datestr)
                    print date

                    # find news content in url
                    reqNews = requests.get(urlNews)
                    soupNews = BeautifulSoup(reqNews.text, "lxml")

                    titleNews = soupNews.find('title').get_text()
                    print titleNews
                    newsKeywords = soupNews.find('meta', {'name': 'news_keywords'})
                    keyword = ''
                    if newsKeywords is not None:
                        keyword = newsKeywords.get('content')
                    print keyword

                    description = soupNews.find('meta', {'name': 'description'}).get('content')
                    print description
                    section = soupNews.find('meta', {'itemprop': 'articleSection'}).get('content')
                    print section

                    # find news content
                    newsContent = soupNews.find("div", {'class': 'read'})

                    # find paragraph in news content
                    if newsContent != None:
                        for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                            _ = elm.extract()
                        for elm in newsContent.findAll("div", {"id": re.compile('div-gpt-ad.*')}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("div", {'class': 'recomendationnews'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("div", {'class': 'detail-tag'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("div", {'class': 'paging'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all('noscript'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('iframe'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('script'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('p'):
                            temp = elm.get_text().lower().encode('utf-8')
                            if 'baca juga :' in temp or 'baca juga:' in temp :
                                _ = elm.extract()
                        for elm in newsContent.find_all('a'):
                            del elm['href']
                            del elm['rel']
                            del elm['target']
                            del elm['title']
                        for elm in newsContent.find_all('img'):
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
                        newsDict['content'] = content
                        newsDict['keyword'] = keyword
                        newsDict['description'] = description
                        newsDict['category'] = section
                        newsDict['source'] = 'okezone'
                        result.append(newsDict)
                        db.save(newsDict)
            except Exception, err:
                print err

        return result

    def formatDate(self, date):
        d, m, y, h = date.split(' ')
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
        return d + '-' + mm + '-' + y + ' ' + h + ':00'

    def crawl(self):
        self.crawl_content()






