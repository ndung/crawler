from datetime import date, datetime, timedelta
import threading
import sys, getopt
from kompas import Kompas
from detik import Detik
from tempo import Tempo
from liputan6 import Liputan6
from republika import Republika
from merdeka import Merdeka
from okezone import Okezone
from cnn import CNN
from antara import Antara
from jawapos import JawaPos
from sindonews import Sindonews
from suara import Suara
from dateutil.parser import parse

thread_dict = {}


class CrawlingThread(threading.Thread):

    def __init__(self, media_online, start_date, end_date):
        threading.Thread.__init__(self)
        self.media_online = media_online
        self.start_date = start_date
        self.end_date = end_date
        self.is_running = True
        thread_dict[self.media_online] = self

    def run(self):
        print("Start crawling " + self.media_online)
        if self.media_online == 'detik':
            detik = Detik()
            detik.crawl(self.start_date, self.end_date)
        elif self.media_online == 'kompas':
            kompas = Kompas()
            kompas.crawl(self.start_date, self.end_date)
        elif self.media_online == 'tempo':
            tempo = Tempo()
            tempo.crawl(self.start_date, self.end_date)
        elif self.media_online == 'liputan6':
            liputan6 = Liputan6()
            liputan6.crawl(self.start_date, self.end_date)
        elif self.media_online == 'republika':
            republika = Republika()
            republika.crawl(self.start_date, self.end_date)
        elif self.media_online == 'merdeka':
            merdeka = Merdeka()
            merdeka.crawl(self.start_date, self.end_date)
        elif self.media_online == 'cnn':
            cnn = CNN()
            cnn.crawl(self.start_date, self.end_date)
        elif self.media_online == 'sindonews':
            sindonews = Sindonews()
            sindonews.crawl(self.start_date, self.end_date)
        elif self.media_online == 'okezone':
            okezone = Okezone()
            okezone.crawl()
        elif self.media_online == 'antara':
            antara = Antara()
            antara.crawl()
        elif self.media_online == 'jawapos':
            jawapos = JawaPos()
            jawapos.crawl()
        elif self.media_online == 'suara':
            suara = Suara()
            suara.crawl()
        self.is_running = True

    def stop(self):
        # del thread_dict[self.media_online]
        if self.is_running:
            print("Stop crawling " + self.media_online)
            self.is_running = False


def run():
    for k, t in thread_dict.items():
        if not t.is_alive():
            print("thread " + k + " is not alive")
            del thread_dict[k]

    start_date = date(2019, 2, 1)
    end_date = date(2019,2, 10)

    media_onlines = ['detik','kompas','tempo','liputan6','republika','merdeka','cnn','sindonews','okezone']
    for media_online in media_onlines:
        if not thread_dict.has_key(media_online):
            t = CrawlingThread(media_online, start_date, end_date)
            t.start()
        elif thread_dict.has_key(media_online):
            t = thread_dict[media_online]
            t.stop()
    #threading.Timer(1.0, run).start()


def main(argv):
    run()


if __name__ == '__main__':
    main(sys.argv[1:])
