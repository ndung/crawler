from dbconn import DBConn
from bs4 import BeautifulSoup, Comment
from datetime import timedelta, datetime
import requests
import re

class Republika:
    def crawl_content(self, url):
        result = []
        # find link page
        print url

        for i in range(0, 20):

            try:
                # find article link
                req = requests.get(url+'/'+str(i*20))
                print 'url:'+req.url
                soup = BeautifulSoup(req.text, "lxml")

                newsLink = soup.find_all("div", {'class': 'txt_subkanal txt_index'})
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

                    titleNews = soupNews.find('title').get_text()
                    print titleNews
                    keyword = soupNews.find('meta', {'name': 'keywords'}).get('content')
                    description = soupNews.find('meta', {'name': 'description'}).get('content')
                    section = soupNews.find('meta', {'property': 'article:section'}).get('content')
                    datestr = soupNews.find('meta', {'property': 'article:published_time'}).get('content').replace('T', ' ')
                    date = datestr[0:19]
                    print date

                    # find news content
                    newsContent = soupNews.find("div", {'class': 'artikel'})

                    if newsContent != None:
                        for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                            _ = elm.extract()
                        for elm in newsContent.find_all("div", {'class': re.compile('ads.*')}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("div", {'class': 'parallax'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("div", {'class': 'picked-article'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("div", {'class': 'taiching'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all('div'):
                            temp = elm.get_text().lower().encode('utf-8').strip()
                            if temp == '':
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

                        newsContent['class'] = 'news'
                        del newsContent['itemprop']

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
                        newsDict['source'] = 'republika'
                        result.append(newsDict)
                        db.save(newsDict)
            except Exception, err:
                print err

        return result

    def daterange(self, startDate, endDate):
        for n in range(int ((endDate - startDate).days)):
            yield startDate + timedelta(n)

    def crawl(self, startDate, endDate):
        for single_date in self.daterange(startDate, endDate):
            datenews = str(single_date.strftime("%Y/%m/%d"))
            url = 'https://republika.co.id/index/' + datenews
            self.crawl_content(url)





