import requests
from bs4 import BeautifulSoup

def get_sections(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content,"lxml")
    nav = soup.find('nav',{'id':"main-nav"})
    lis = nav.findAll('a')
    all_sections = []
    for i in lis:
        if len(i.text.strip()) > 2:
            if 'video' in i.text.strip():
                continue
            if i['href'].startswith('http'):
                real_link = str(i['href'])
            else:
                real_link =\
                'https://timesofindia.indiatimes.com'+str(i['href'])

            sections = {'section':i.text.strip(),'link':real_link}
            all_sections.append(sections)
    return all_sections 
def get_links_sections(section_link,section_name):
    r = requests.get(section_link)
    soup = BeautifulSoup(r.content,"lxml")
    ahref = soup.findAll('a')
    article_links = []
    for ah in ahref:
        try:
            if ah['href'].endswith('.cms'):
                if ah['href'].startswith('http'):
                    real_link = ah['href']
                else:
                    real_link = \
                    'https://timesofindia.indiatimes.com'+str(ah['href'])
                if 'video' in real_link:
                    continue
                else:
                    art_link = {'section':section_name,'link':real_link}
                    article_links.append(art_link)
        except Exception as e:
            print(str(e))
    return article_links


def get_article(link):
    content = {}
    r = requests.get(link)
    soup = BeautifulSoup(r.content,"lxml")
    main_content = soup.find('div',{'class':'main-content'})
    art_head = main_content.find('arttitle')
    content['title'] = art_head.text.strip()
    time_span = main_content.find('span',{'class':'time_cptn'})
    content['date'] = time_span.text.strip()
    body_div = main_content.find('div',{'class':'Normal'})
    content['body'] = body_div.text.strip()
    content['link'] = link
    return content
    

