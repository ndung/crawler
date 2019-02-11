from dbconn import DBConn
from bs4 import BeautifulSoup, Comment
from datetime import timedelta, datetime
import requests
import re

class Kompas:
    def crawl_content(self, url):
        result = []
        try:
            req = requests.get(url)
            soup = BeautifulSoup(req.text, "lxml")

            # find paging page
            paging = soup.find_all("div", {'class': 'paging clearfix'})
            lastPage = None
            if len(paging) != 0:
                paging_link = paging[0].find_all('a', {'class': 'paging__link'})
                if len(paging_link) == 4:
                    lastPage = int(4)
                else:
                    lastPage = int([item.get('href').split('/')[-1] for item in paging_link][-1]) + 1
            else:
                lastPage = int(2)

            db = DBConn()

            # looping through paging
            for i in range(1, lastPage):
                print url + "/" + str(i)

                # find article link
                req = requests.get(url + "/" + str(i))
                soup = BeautifulSoup(req.text, "lxml")
                newsLink = soup.find_all("div", {'class': 'article__list clearfix'})
                print newsLink

                # looping through article link
                for idx, news in enumerate(newsLink):
                    newsDict = {}
                    # find urll news
                    urlNews = news.find('a', {'class': 'article__link'}).get('href')
                    print urlNews

                    # find news content in url
                    reqNews = requests.get(urlNews)
                    soupNews = BeautifulSoup(reqNews.text, "lxml")

                    titleNews = soupNews.find('title').get_text()
                    print titleNews
                    date = soupNews.find('meta', {'name': 'content_PublishedDate'}).get('content')
                    print date
                    keyword = soupNews.find('meta', {'name': 'keywords'}).get('content')
                    description = soupNews.find('meta', {'name': 'description'}).get('content')
                    category = soupNews.find('meta', {'name': 'content_category'}).get('content')

                    # find news content
                    newsContent = soupNews.find("div", {'class': 'read__content'})

                    # find paragraph in news content
                    if newsContent != None:

                        newsContent['class'] = 'news'

                        for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                            _ = elm.extract()
                        for elm in newsContent.findAll("div", {"id": re.compile('div-gpt-ad.*')}):
                            _ = elm.extract()
                        for elm in newsContent.findAll("div", {"id": re.compile('.*widget.*')}):
                            _ = elm.extract()
                        for elm in newsContent.findAll("div", {"class": "video"}):
                            _ = elm.extract()
                        for elm in newsContent.findAll("div", {"class": "ads"}):
                            _ = elm.extract()
                        for elm in newsContent.findAll("div", {"class": "photo-infographic"}):
                            _ = elm.extract()
                        for elm in newsContent.findAll("div", {"class": "comp-embedded-float-right"}):
                            _ = elm.extract()
                        for elm in newsContent.findAll("div", {"class": "photo"}):
                            _ = elm.extract()
                        for elm in newsContent.findAll("div", {"class": "fb-quote"}):
                            _ = elm.extract()
                        for elm in newsContent.find_all('a'):
                            del elm['href']
                            del elm['target']
                            del elm['rel']
                            del elm['title']
                        for elm in newsContent.find_all('p'):
                            temp = elm.get_text().lower().encode('utf-8')
                            if 'baca juga :' in temp or 'baca juga:' in temp :
                                _ = elm.extract()
                        for elm in newsContent.find_all('img'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('script'):
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
                        newsDict['category'] = category
                        newsDict['source'] = 'kompas'
                        result.append(newsDict)

                        db.save(newsDict)
        except Exception as e:
            print e
            pass

        return result

    def daterange(self, startDate, endDate):
        for n in range(int((endDate - startDate).days)):
            yield startDate + timedelta(n)

    def crawl(self, startDate, endDate):
        for single_date in self.daterange(startDate, endDate):
            url = 'https://indeks.kompas.com/news/' + single_date.strftime("%Y-%m-%d")
            self.crawl_content(url)
