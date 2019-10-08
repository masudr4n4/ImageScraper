import requests
from bs4 import BeautifulSoup as B
import sqlite3
import time
import os
path = 'Database'

def save_to_db(data):
  connection = sqlite3.connect(os.path.join(path,'CoinMarketCapData.db'))
  c = connection.cursor()
  command = '''Insert into CoinMarketData values('{0}','{1}','{2}','{3}','{4}','{5}')'''
  sql_command = command.format(*data)
  c.execute(sql_command)
  connection.commit()
  connection.close()
  print('done')


def parser(i):
  coin = i.find('td',class_='no-wrap currency-name').text.split()
  Symble= coin[0]
  Name =coin[1]
  Cap = i.find('td',class_='no-wrap market-cap text-right').text.strip().replace(',','').replace('$','')
  price = i.find('a',class_='price').text.replace(',','').replace('$','')
  supply = i.find('td',class_='no-wrap text-right circulating-supply').text.strip().replace(',','').replace('$','')
  volume = i.find('a',class_='volume').text.strip().replace(',','').replace('$','')
  data = (Name,Symble,int(str(Cap).strip()),int(str(price).strip()),str(supply).strip(),str(volume).strip())
  return data



def parsing_page(url):
  header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0'
  }
  page = requests.get(url,headers=header)
  print('Received status code {0}'.format(page.status_code))
  soup = B(page.content,'html.parser')
  for i in soup.find_all('tr')[1:]:
    print('working on it')
    try:
      data = parser(i)
      save_to_db(data)
    except Exception as e:
      print('Something happen wrong {0}'.format(e))

if __name__=="__main__":
    print('started your work')
    url_list = ['https://coinmarketcap.com/{0}/'.format(i) for i  in range(1,21)]
    s = time.perf_counter()
    counter = 1 
    for i in url_list:
        print('working with page numeber = {0}'.format(counter))
        parsing_page(i)
        counter+=1
        time.sleep(5)
    e = time.perf_counter()
    print('DOne')
    print('Done the jobs in {0}'.format(e-s))




