from dbconn import DBConn
from bs4 import BeautifulSoup, Comment
from datetime import timedelta, datetime
import requests
import re

class JawaPos:
    def crawl_content(self):
        result = []
        # find link page

        for i in range(0, 20):
            try:
                # find article link
                req = requests.get('https://www.jawapos.com/berita-hari-ini/page='+str(i))

                print req.url
                soup = BeautifulSoup(req.text, "lxml")

                newsLink = soup.find_all("div", {'class': 'submenu-article'})

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
                    date = soupNews.find('meta', {'property': 'article:published_time'}).get('content')
                    print date
                    keyword = soupNews.find('meta', {'name': 'keywords'}).get('content')
                    description = soupNews.find('meta', {'name': 'description'}).get('content')
                    category = ''
                    # find news content
                    newsContent = soupNews.find("article", {'class': 'article'})

                    # find paragraph in news content
                    if newsContent != None:
                        for elm in newsContent.findAll("div", {"class": "article-tags"}):
                            _ = elm.extract()
                        for elm in newsContent.findAll("section", {"class": "banner-ads"}):
                            _ = elm.extract()
                        for elm in newsContent(text=lambda text: isinstance(text, Comment)):
                            _ = elm.extract()
                        for elm in newsContent.find_all('a'):
                            del elm['href']
                            del elm['rel']
                            del elm['target']
                            del elm['title']
                        for elm in newsContent.find_all('figure'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('img'):
                            _ = elm.extract()
                        for elm in newsContent.find_all('script'):
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
                        newsDict['source'] = 'jawapos'
                        result.append(newsDict)
                        db.save(newsDict)
            except Exception as e:
                print e
                pass

        return result

    def crawl(self):
        self.crawl_content()





