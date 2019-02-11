from dbconn import DBConn
from bs4 import BeautifulSoup, Comment
from datetime import timedelta, datetime
import requests
import re

class Antara:
    def crawl_content(self):
        result = []
        # find link page

        for i in range(1, 20):
            try:
                # find article link
                req = requests.get('https://www.antaranews.com/terkini/'+str(i))

                print req.url
                soup = BeautifulSoup(req.text, "lxml")

                newsLink = soup.find_all("article", {'class': 'simple-post'})

                db = DBConn()

                # looping through article link
                for idx, news in enumerate(newsLink):
                    newsDict = {}
                    # print news

                    # find urll news
                    urlNews = news.find('a').get('href')
                    print urlNews

                    if not urlNews.startswith('https://www.antaranews.com/foto'):
                        # find news content in url
                        reqNews = requests.get(urlNews)
                        soupNews = BeautifulSoup(reqNews.text, "lxml")

                        titleNews = soupNews.find('title').get_text()
                        print titleNews
                        datetime = soupNews.find('meta', {'itemprop': 'datePublished'}).get('content').replace('T', ' ')
                        date = datetime[0:19]
                        print date
                        keyword = ''
                        description = soupNews.find('meta', {'name': 'description'}).get('content')
                        category = soupNews.find('meta', {'property': 'article:section'}).get('content')
                        # find news content
                        newsContent = soupNews.find("div", {'class': 'post-content'})

                        # find paragraph in news content
                        if newsContent!=None :
                            for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                                _ = elm.extract()
                            for elm in newsContent.findAll("blockquote", {"class": "instagram-media"}):
                                _ = elm.extract()
                            for elm in newsContent.find_all('b'):
                                temp = elm.get_text().lower().encode('utf-8')
                                if 'baca juga :' in temp or 'baca juga:' in temp:
                                    _ = elm.extract()
                            for elm in newsContent.find_all('a'):
                                del elm['href']
                                del elm['rel']
                                del elm['target']
                                del elm['title']
                            for elm in newsContent.find_all('img'):
                                _ = elm.extract()
                            for elm in newsContent.findAll("ul", {"class": "blog-tags"}):
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
                            newsDict['source'] = 'antara'
                            result.append(newsDict)
                            db.save(newsDict)
            except Exception as e:
                print e
                pass

        return result

    def crawl(self):
        self.crawl_content()





