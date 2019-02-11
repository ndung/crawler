from dbconn import DBConn
from bs4 import BeautifulSoup, Comment
from datetime import timedelta, datetime
import requests
import re

class Liputan6:
    def crawl_content(self, url):
        result = []
        # find link page
        print url

        for i in range(1, 20):

            try:
                # find article link
                req = requests.get(url+'?page='+str(i))
                print 'url:'+req.url
                soup = BeautifulSoup(req.text, "lxml")
                newsLink = soup.find_all("article", {'class': 'articles--rows--item'})
                print newsLink
                db = DBConn()

                # looping through article link
                for idx, news in enumerate(newsLink):

                    newsDict = {}

                    # find urll news
                    urlNews = news.find('a').get('href')
                    print urlNews

                    datestr = news.find('time').get('datetime')
                    date = datestr[0:4]+'-'+datestr[5:7]+'-'+datestr[8:10]+' '+datestr[11:19]
                    print date

                    # find news content in url
                    reqNews = requests.get(urlNews)
                    soupNews = BeautifulSoup(reqNews.text, "lxml")

                    titleNews = soupNews.find('meta', {'name': 'title'}).get('content')
                    print titleNews
                    keyword = soupNews.find('meta', {'name': 'keywords'}).get('content')
                    description = soupNews.find('meta', {'name': 'description'}).get('content')
                    category = soupNews.find('meta', {'name': 'adx:sections'}).get('content')

                    # find news content
                    newsContent = soupNews.find("div", {'class': 'article-content-body__item-content'})

                    if newsContent != None:

                        newsContent['class'] = 'news'
                        del newsContent['data-component-name']

                        for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                            _ = elm.extract()
                        for elm in newsContent.findAll("div", {"id": re.compile('div-gpt-ad.*')}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("div", {'class': 'baca-juga'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("div", {'class': 'seamless-ads'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("ul", {'class': 'baca-juga__list'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("p", {'class': 'baca-juga__header'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("p", {'class': 'read-page--header--author__datetime-wrapper'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all('script'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('a'):
                            del elm['href']
                            del elm['target']
                            del elm['rel']
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
                        newsDict['source'] = 'liputan6'
                        newsDict['category'] = category
                        result.append(newsDict)
                        db.save(newsDict)
            except Exception, err:
                print err
                pass

        return result

    def daterange(self, startDate, endDate):
        for n in range(int ((endDate - startDate).days)):
            yield startDate + timedelta(n)

    def crawl(self, startDate, endDate):
        for single_date in self.daterange(startDate, endDate):
            datenews = str(single_date.strftime("%Y/%m/%d"))
            url = 'https://www.liputan6.com/indeks/' + datenews
            self.crawl_content(url)






