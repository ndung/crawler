from dbconn import DBConn
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import requests
import re

class CNN:
    def crawl_content(self, url):
        result = []
        # find link page

        for i in range(1, 9):
            try:
                # find article link
                req = requests.get(url+'&p='+str(i))
                print req.url
                soup = BeautifulSoup(req.text, "lxml")

                newsLink = soup.find("div", {'class': 'l_content'}).find_all('article')

                db = DBConn()

                # looping through article link
                for idx, news in enumerate(newsLink):
                    newsDict = {}
                    # print news

                    # find urll news
                    urlNews = news.find('a').get('href')
                    print urlNews

                    reqNews = requests.get(urlNews)
                    soupNews = BeautifulSoup(reqNews.text, "lxml")

                    # find news content
                    titleNews = soupNews.find('title').get_text()
                    print titleNews
                    newsContent = soupNews.find("span", {'id': 'detikdetailtext'})
                    date = soupNews.find('meta', {'name': 'publishdate'}).get('content')
                    keyword = soupNews.find('meta', {'name': 'keyword'}).get('content')
                    description = soupNews.find('meta', {'name': 'description'}).get('content')
                    category = soupNews.find('meta', {'name': 'dtk:namakanal'}).get('content')
                    contentType = soupNews.find('meta', {'name': 'contenttype'}).get('content')

                    # find paragraph in news content
                    if contentType != 'singlepagevideo' and contentType!= 'multiplefotophoto' and newsContent!=None :
                        for elm in newsContent.find_all('img'):
                            _ = elm.extract()
                        for elm in newsContent.find_all("div", {'class': 'lihatjg'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("table", {'class': 'linksisip'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("table", {'class': 'topiksisip'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all("table", {'class': re.compile('.*pic_artikel_sisip_table.*')}):
                            _ = elm.extract()
                        for elm in newsContent.find_all('script'):
                            _ = elm.extract()
                        for elm in newsContent.find_all("a", {'class': 'embed'}):
                            _ = elm.extract()
                        for elm in newsContent.find_all('a'):
                            del elm['href']
                            del elm['rel']
                            del elm['target']
                            del elm['title']

                        newsContent['class'] = 'news'
                        del newsContent['id']

                        content = newsContent.prettify().encode('utf-8').strip()

                        print content

                        # wrap in dictionary
                        newsDict['date'] = date.replace('/','-')
                        newsDict['url'] = urlNews
                        newsDict['title'] = titleNews
                        newsDict['keyword'] = keyword
                        newsDict['description'] = description
                        newsDict['content'] = content
                        newsDict['category'] = category
                        newsDict['source'] = 'cnn'
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
            url = 'https://www.cnnindonesia.com/indeks?date=' + datenews
            self.crawl_content(url)





