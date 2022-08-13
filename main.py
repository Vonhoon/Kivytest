import math

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from kivy.uix.label import Label
import webbrowser
import requests
from bs4 import BeautifulSoup
import datetime

from kivy.clock import Clock

totalpages = 30 * 3
key = ""
pages = 20
date_range = 30


products = []  # List to store name of the product
link = []
website = []
time = []

e = datetime.datetime.now()
today = e.strftime("%Y.%m.%d")
datelimit = (e - datetime.timedelta(days=date_range)).strftime("%Y.%m.%d")

class Hyperlink(Label):
    def __init__(self, **kwargs):
      self.target = kwargs.pop('target')
      kwargs['markup'] = True
      kwargs['color'] = (.5,.8,.9,1)
      kwargs['text'] = "[u][ref=link]{}[/ref][/u]".format(kwargs['text'])
      kwargs['on_ref_press'] = self.link
      super().__init__(**kwargs)
      self.bind(
          width=lambda *x:
          self.setter('text_size')(self, (self.width, None)),
          texture_size=lambda *x: self.setter('height')(self, self.texture_size[1]))

    def link(self, *args):
      webbrowser.open(self.target)

class Padding(Label):
    pass

class Top(BoxLayout):
    ruliweb_on = BooleanProperty(True)
    clien_on = BooleanProperty(True)
    coolenjoy_on = BooleanProperty(True)
    ppomppu_on = BooleanProperty(True)

    def on_slider_value(self, widget):
        global date_range
        date_range = int(widget.value)

    def on_text_validate(self, input, button, widget):
        self.on_button_press(input, button, widget)

    def on_focus(self, widget):
        if widget.focus:
            if widget.selection_text == "":
                Clock.schedule_once(lambda dt: widget.select_all())

    def on_button_press(self, input, button, widget):
        global key
        global products
        global link
        global website
        global time
        global totalpages
        global datelimit

        e = datetime.datetime.now()
        datelimit = (e - datetime.timedelta(days=date_range)).strftime("%Y.%m.%d")
        key = str(input.text)
        button.active = False
        button.text = "찾는 중..."
        if key == "" or key == "검색창":
            key = " "

        widget.clear_widgets(widget.children)
        products.clear()
        link.clear()
        website.clear()
        time.clear()

        if self.ruliweb_on:
            ruliweb(key)
        if self.clien_on:
            clien(key)
        if self.ppomppu_on and key != " ":
            ppomppu(key)
        if self.coolenjoy_on:
            coolenjoy(key)

        totalpages = (len(products) * 3)
        padding = Label(text="   ", size_hint=(0.3, 1))

        if self.ruliweb_on or self.clien_on or self.ppomppu_on or self.coolenjoy_on:

            for i in range(0, totalpages):
                # size = dp(100) + i * 10
                if i < 3:
                    showtext = "              "
                    size = 0.33
                    b = Label(text=showtext, size_hint=(size, 1), font_name="fonts/GmarketSansTTFBold.ttf",
                              font_size="12dp")  # this will be shown first then kivy file
                    widget.add_widget(b)
                else:
                    line = math.floor(i / 3) - 1
                    print("working on line: " + str(line))
                    if i % 3 == 0:
                        showtext = time[line]
                        size = 0.05
                        b = Label(text=showtext, size_hint=(size, 1), font_name="fonts/GmarketSansTTFBold.ttf",
                                  font_size="10dp")  # this will be shown first then kivy file
                        widget.add_widget(b)
                    elif i % 3 == 1:
                        showtext = website[line]
                        b = Label(text=showtext, size_hint=(None, None), size=("10dp", "10dp"), font_name="fonts/GmarketSansTTFBold.ttf",
                                  font_size="10dp")  # this will be shown first then kivy file
                        widget.add_widget(b)
                    elif i % 3 == 2:
                        showtext = products[line]
                        size = 1.5
                        b = Hyperlink(text=showtext, size_hint=(size, None),
                                      font_name="fonts/GmarketSansTTFBold.ttf",
                                      font_size="12dp", target=link[line])  # this will be shown first then kivy file
                        widget.add_widget(b)

            widget.add_widget(padding)
        else:
            for i in range(3):
                widget.add_widget(Padding())
            warning = Label(text="선택한 사이트가 없습니다!", size_hint=(1, 1), font_name="fonts/GmarketSansTTFBold.ttf", font_size="16dp")
            widget.add_widget(warning)

        button.text = "Search!"
        button.active = True

    def openweb(self, link):
        webbrowser.open(link)

    def ruliweb_switch(self, widget):
        if widget.active:
            self.ruliweb_on = True
        else:
            self.ruliweb_on = False

    def ppomppu_switch(self, widget):
        if widget.active:
            self.ppomppu_on = True
        else:
            self.ppomppu_on = False

    def clien_switch(self, widget):
        if widget.active:
            self.clien_on = True
        else:
            self.clien_on = False

    def coolenjoy_switch(self, widget):
        if widget.active:
            self.coolenjoy_on = True
        else:
            self.coolenjoy_on = False


class fiveducksApp(App):
    pass


def ruliweb(keyword):
    url = "\fhttps://bbs.ruliweb.com/market/board/1020?search_type=subject&search_key={}".format(keyword)
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    body = soup.find(attrs={"class": "board_main theme_default theme_white"})
    i = 0
    for a in body.findAll('tr', attrs={'class': 'table_body blocktarget'}):
        if i < pages:
            if len(a.find('td', attrs={'class': 'time'}).text.strip()) < 6:
                rtimestamp = today
            else:
                rtimestamp = a.find('td', attrs={'class': 'time'}).text.strip()
            if datetime.datetime.strptime(rtimestamp, "%Y.%m.%d") < datetime.datetime.strptime(datelimit, "%Y.%m.%d"):
                i = pages
            else:
                time.append(rtimestamp)
                deal = a.find('a', attrs={'class': 'deco'}, href=True)
                products.append(deal.text)
                link.append(deal.get("href"))
                website.append("Ruliweb")
                i += 1


def yepan(keyword):
    url = "\fhttp://yepan.net/bbs/board.php?bo_table=local_info&sca=&sfl=wr_subject&stx={}&sop=and&x=0&y=0".format(
        keyword)
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    body = soup.select_one('#fboardlist > table > tbody')
    for a in body.select('td.mw_basic_list_subject > div.mw_basic_list_subject_desc'):
        print(a)
        products.append(a.text)
        link.append(a.select('a')[-1]['href'])
        website.append("Yepan")
    for b in body.findAll('td', attrs={'class': 'mw_basic_list_datetime'}):
        timestamp = b.text
        time.append(timestamp)


def clien(keyword):
    url = "\fhttps://www.clien.net/service/search?q={}&sort=recency&boardCd=jirum&isBoard=true".format(keyword)
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    body = soup.find(attrs={"class": "contents_jirum"})

    i = 0
    for b in body.findAll('span', attrs={'class': 'timestamp'}):
        if i < pages:
            if b.text[0:10].replace('-', '.') < datelimit:
                i = pages
            else:
                time.append(b.text[0:10].replace('-', '.'))
            if i < pages:
                deal = body.findAll('span', attrs={'class': 'list_subject'})[i].find('a',
                                                                                     attrs={'class': 'subject_fixed'},
                                                                                     href=True)
                products.append(deal.get("title"))
                link.append("https://www.clien.net" + deal.get("href"))
                website.append("Clien")
                i += 1


def coolenjoy(keyword):
    url = "\fhttps://coolenjoy.net/bbs/jirum?bo_table=jirum&sca=&sop=and&sfl=wr_subject&stx={}".format(keyword)
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    body = soup.find('tbody')
    i = 0
    if keyword == " ":
        for b in body.findAll('td', attrs={'class': 'td_date'}):
            if i == 0:
                i += 1
            else:
                if i < pages + 1:
                    if len(b.text[0:10].replace('-', '.').strip()) < 6:
                        cdate = today
                    else:
                        cdate = '20' + b.text[0:10].replace('-', '.').strip()
                    if cdate < datelimit:
                        i = pages
                    else:
                        time.append(cdate)
                    if i < pages + 1:
                        deal = body.findAll('td', attrs={'class': 'td_subject'})[i].text.strip()
                        products.append(deal)
                        link.append(body.findAll('td', attrs={'class': 'td_subject'})[i].find('a').get("href"))
                        website.append("Coolenjoy")
                        i += 1
    else:
        for b in body.findAll('td', attrs={'class': 'td_date'}):
            if i < pages:
                if len(b.text[0:10].replace('-', '.').strip()) < 6:
                    cdate = today
                else:
                    cdate = '20' + b.text[0:10].replace('-', '.').strip()
                if cdate < datelimit:
                    i = pages
                else:
                    time.append(cdate)
                if i < pages:
                    deal = body.findAll('td', attrs={'class': 'td_subject'})[i].text.strip()
                    products.append(deal)
                    link.append(body.findAll('td', attrs={'class': 'td_subject'})[i].find('a').get("href"))
                    website.append("Coolenjoy")
                    i += 1


def ppomppu(keyword):
    trskip = 5
    url = "\fhttps://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page_num=20&category=&search_type=sub_memo&keyword={}".format(
        keyword)
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    body = soup.select_one('#revolution_main_table > tbody')

    i = 0

    for a in body.select('tr'):
        if i > trskip and i < pages * 30:
            if i % 3 == 0:
                timestamp = a.select_one('td:nth-of-type(1) > a > img')
                try:
                    ptime = timestamp.get('src')[-14:-10] + '.' + timestamp.get('src')[-10:-8] + '.' + timestamp.get(
                        'src')[-8:-6]
                    datetime.datetime.strptime(ptime, '%Y.%m.%d')
                except:
                    ptime = a.select_one('td:nth-of-type(1) > a').get('href')[-6:]
                if ptime < datelimit:
                    i = pages * 30
                else:
                    time.append(ptime)
                    deal = a.select_one('td:nth-of-type(2) > div')
                    products.append(deal.text)
                    link.append('https://ppomppu.co.kr/zboard/' + deal.select_one('a')['href'])
                    website.append("Ppomppu")
                    i += 1
            else:
                i += 1
        else:
            i += 1


fiveducksApp().run()
