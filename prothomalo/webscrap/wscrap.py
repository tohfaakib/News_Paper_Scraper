from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


#Global variable
base_url = "https://www.prothomalo.com"


class NewsScraper:
    flag = False
    filepath = ''
    filepath_html = ''
    __category = ''
    __url = ''
    __data = ''
    __wlog = None
    __soup = None

    def __init__(self, category, wlog):
        self.__url = base_url+'/'+category
        self.filepath = 'html/{}.html'.format(category)
        self.filepath_html = 'html/page/{}.html'.format(category)
        self.__wlog = wlog
        self.__category = category



    def retrieve_webpage(self):
        try:
            html = urlopen(self.__url)
        except Exception as e:
            print(e)
            self.__wlog.report(e)
        else:
            self.__data = html.read()
            if len(self.__data) > 0:
                print("Retrieved Successfully")



    def write_webpage_as_html(self, filepath=filepath_html, data=''):
        try:
            with open(filepath, 'wb') as fobj:
                if data:
                    fobj.write(data)
                else:
                    fobj.write(self.__data)
        except Exception as e:
            print(e)
            self.__wlog.report(str(e))




    def read_webpage_from_html(self, filepath=filepath_html):
        try:
            with open(filepath, encoding='UTF-8') as fobj:
                self.__data = fobj.read()
        except Exception as e:
            print(e)
            self.__wlog.report(e)




    def convert_data_to_bs4(self):
        self.__soup = BeautifulSoup(self.__data, "html.parser")




    def parse_soup_to_simple_html(self):
        news_list = self.__soup.find_all(['h2'])

        htmltext = '''
<html>
    <head>
    <meta charset="UTF-8">
    <title>Prothom Alo Link Scraping</title>
    </head>
    <body>
        {NEWS_LINKS}
    </body>
</html>     

'''
        cat = "<h2>{}</h2>\n".format(self.__category.title())
        news_links = cat
        news_links += '<ol>'

        for tag in news_list:
            img_link = ''
            if tag.parent.parent.select_one("a"):
                href = tag.parent.parent.a.get('href')
                link = base_url + href

                h_title = tag.select_one(".title")
                title = self.cleanhtml(h_title)

                h_summery = tag.parent.select_one("div")
                summery = self.cleanhtml(h_summery)

                images = tag.parent.parent.div.findAll('img')

                for image in images:
                    img_src = image['src']
                    if img_src:
                        img_link = 'https:'+str(img_src)


                if self.avoid_el(title, href):
                    description = self.description_parser(link)

                    news_links += "<li><a href='{}' target='_blank' >{}</a><br><p>[{}]</p><br>\n".format(link, title, summery)
                    news_links += '<img src="{}">'.format(img_link)
                    news_links += '<p>{}</p>'.format(description)


        news_links += '</ol>'

        htmltext = htmltext.format(NEWS_LINKS=news_links)

        self.write_webpage_as_html(filepath=self.filepath, data=htmltext.encode())





    def description_parser(self, link):
        try:
            desc = ""
            self.__url = link
            self.retrieve_webpage()
            self.convert_data_to_bs4()
            news_body = self.__soup.findAll('div', itemprop='articleBody')
            for p_tag in news_body:
                p_tag = p_tag.findAll('p')

                for p in p_tag:
                    des = p.text
                    desc = desc+"\r\n\r\n"+des+"\n\n\n"
                if desc:
                    print("description fetched!")

            return desc
        except:
            pass


    def avoid_el(self, title, href):
        try:
            i = 0
            p = 0
            h_arr = []
            for j in list(href):
                if j == '/':
                    i = i + 1

            for w in href.split('/'):
                word = w.strip()
                if word == 'gallery' or word == 'video' or word == 'photo':
                    self.flag = True
                    break
                #not to loop through all the line
                p = p + 1
                if p > 4:
                    break

            if not i == 1:
                if not self.flag:
                    if title:
                        return True
        except:
            pass

    def cleanhtml(self, text):
        try:
            clean_text = re.sub('<[^<]+?>', '', str(text))
            return clean_text
        except:
            pass


    def change_url(self, url):

        self.__url = url

    def print_data(self):
        print(self.__data)