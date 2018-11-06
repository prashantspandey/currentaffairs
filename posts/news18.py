from bs4 import BeautifulSoup
import requests
from more_itertools import unique_everseen
import pickle


def get_categories(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")
    nav = soup.findAll('div')
    category_address = []
    for na in nav:
        try:
            if 'outerone' in na['class']:
                cats = na.findAll('a')
                for i in cats:
                    if len(i.text) > 2:
                        print(i.text)
                        if 'https://www.news18.com' in i['href']:
                            pass
                        else:
                            link = 'https://www.news18.com'+str(i['href'])
                            
                        category = {'name':i.text.strip(),'link':link}
                        category_address.append(category)


        except Exception as e:
            pass
    category_address = list(unique_everseen(category_address))
    return category_address

def get_links(category_address):
    overall_news = []
    try:
        for ca in category_address:
            link = ca['link']
            cat = ca['name']
            r = requests.get(link)
            soup = BeautifulSoup(r.content,"lxml")
            atags = soup.findAll('a')
            for atag in atags:
                if len(atag.text.strip()) > 20:
                    link = atag['href']
                    text = atag.text.strip()
                    link_dict = {'newsItem':text,'link':link,'category':cat}
                    overall_news.append(link_dict)
    except Exception as e:
        print(str(e))
    overall_news = list(unique_everseen(overall_news))
    return overall_news

def get_article(ld):
    try:
        all_article = []
        
        content = {}
        link = ld['link']
        cat = ld['category']
        news = ld['newsItem']

        content['link'] = link
        content['category'] = cat
        r = requests.get(link)
        soup = BeautifulSoup(r.content,"lxml")
        headline = soup.findAll('h1')
        for h in headline:
            content['headline'] = h.text.strip()
        description = soup.findAll('div')

        for desc in description:
            try:
                if 'author' in desc['class']:
                    sp = desc.findAll('span')
                    for s in sp:
                        date_text = s.text.strip()
                        date_text = date_text.lower()
                        date_index = date_text.index(':')
                        da = date_text[date_index+1:]
                        content['date'] = da
            except Exception as e:
                pass
        story_heading = soup.findAll('h2',{'class':'story-intro'})
        for sh in story_heading:
            content['story_heading'] = sh.text.strip()
        image_div = soup.findAll('div',{"class":"articleimg"})
        for imd in image_div:
            try:
                img = imd.findAll('picture')
                for im in img:
                    for slayer in im:
                        image_layer = slayer.findAll('img')
                        for s_layer in image_layer:
                            image_src = s_layer['srcset']
                            content['image'] = image_src
                            break
            except Exception as e:
                print(str(e))

        body = soup.findAll('div',{'id':'article_body'})
        for bo in body:
            body_text = bo.text.strip()
            update = body_text.index('update_date')
            body_text = body_text[:update]
            body_text = body_text.replace('\r',' ')
            body_text = body_text.replace('\t',' ')
            Body_text = body_text.replace('\n',' ')
            body_text = body_text.replace('\'',' ')

            content['body'] = body_text
        print(content)
        return content
    except Exception as e:
        print(str(e))


