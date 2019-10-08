import requests
import shutil
import os
from bs4 import BeautifulSoup as B
import time
heder = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
  }
#os.mkdir( os.path.join( os.getcwd(), 'images' ) )
path = "ImageFolder"
if not os.path.exists(path):
  os.makedirs(path)

def send_rq(url):
  page = requests.get(url,headers=heder)
  return page.content


def saving_img(title,link):
  r = requests.get(link,headers=heder,stream=True)
  if r.status_code !=200:
    print('{0}----{1}'.format(link,r.status_code))
  if r.status_code == 200:
    r.raw.decode_content = True
    with open(os.path.join(path,'{0}..png'.format(title[:30])),'wb') as f:
      shutil.copyfileobj(r.raw,f)
    print('Done an image')


def parsing_page(data):
  soup = B(data,'html.parser')
  img_list = []
  for i in soup.find_all('div',class_='single-post')[1:]:
      img_title = i.find('h2').text.strip()
      print(img_title)
      img = i.find('img')['style'].split()[1]
      img_list.append(img)
      saving_img(img_title,img)
  print('Total image link got ={0}'.format(len(img_list)))


if __name__=="__main__":
  print('Work started')
  url_list =list()
  for i in range(1,2):
    url = 'https://www.mlsbd.asia/?paged={0}'.format(i)
    url_list.append(url)
  for i in url_list:
    data = send_rq(i)
    parsing_page(data)
    time.sleep(5)
  print('Done All the work')
