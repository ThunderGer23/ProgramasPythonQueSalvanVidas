# Importing libraries
import bs4 as bs
import sys
import threading
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
import pytube

down = 0
desc = 0
class Page(QWebEnginePage):
    def __init__(self, url):
        self.app = QApplication(sys.argv)
        QWebEnginePage.__init__(self)
        self.html = ''
        self.loadFinished.connect(self._on_load_finished)
        self.load(QUrl(url))
        self.app.exec_()

    def _on_load_finished(self):
        self.html = self.toHtml(self.Callable)
        print('Conectado :3')

    def Callable(self, html_str):
        self.html = html_str
        self.app.quit()


links = []


def exact_link(link):
    vid_id = link.split('=')
    # print(vid_id)
    str = ""
    for i in vid_id[0:2]:
        str += i + "="

    str_new = str[0:len(str) - 1]
    index = str_new.find("&")

    new_link = "https://www.youtube.com" + str_new[0:index]
    return new_link

def DownHilos(link):
    global down
    down += 1
    video = pytube.YouTube(link)
    print("Descargando " + video.title)
    video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
    down -= 1
    return

url = input("Ingresa el link de tu playlist plox :v")
desc = int(input("Ingresa un numero de descargas simultaneas"))
# Scraping and extracting the video
# links from the given playlist url
page = Page(url)
count = 0

soup = bs.BeautifulSoup(page.html, 'html.parser')

for link in soup.find_all('a', id='thumbnail'):
    # not using first link because it is
    # playlist link not particular video link
    if count == 0:
        count += 1
        continue
    else:
        try:
            vid_src = link['href']
        except KeyError:
            print("Terminando Descargas....")
            continue
        #print(vid_src)
        # keeping the format of link to be
        # given to pytube otherwise in some cases
        new_link = exact_link(vid_src)
        while(down >= desc):
            continue
        threading.Thread(target=DownHilos,args=(new_link,)).start()
print("Gracias por volar con aereopinguino, que tenga un buen día")