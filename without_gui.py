import requests
from bs4 import BeautifulSoup
import lxml
import time
import sqlite3
import re
import asyncio
import aiohttp






cookies = {
    'Path': '/',
    'Path': '/',
    'chk': '1',
    '_ga': 'GA1.2.2134112153.1708331097',
    '_gid': 'GA1.2.88012537.1708331097',
    'test_new_features': '810',
    'ab-link-video-stories': '2',
    'news_prior': '%7B%22item0%22%3A5%2C%22item1%22%3A4%2C%22item2%22%3A3%2C%22item3%22%3A2%7D',
    'test_fast_search': '1',
    '_ga_KGL740D7XD': 'GS1.1.1708331097.1.1.1708331767.19.0.716172175',
    '_gcl_au': '1.1.1964028256.1708331097',
    'AMP_TOKEN': '%24NOT_FOUND',
    'ui': 'b72e73797de12181',
    '_504c2': 'http://10.42.5.231:3000',
    '_fbp': 'fb.1.1708331098842.1685686992',
    '__utma': '79960839.2134112153.1708331097.1708331101.1708331101.1',
    '__utmb': '79960839.4.10.1708331101',
    '__utmc': '79960839',
    '__utmz': '79960839.1708331101.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'advanced_search_test': '42',
    'showNewFeatures': '7',
    '__gads': 'ID=0074f90a0ea9bc02:T=1708331102:RT=1708331102:S=ALNI_MZzLV9yrS_4mNN7Qn4_QFoKJGJ4tA',
    '__gpi': 'UID=00000d5c64ac15e7:T=1708331102:RT=1708331102:S=ALNI_MZ0ROSeRx6OAmQDcUeHMSiz_CT_Kg',
    '__eoi': 'ID=6b2210d8bcb1e034:T=1708331102:RT=1708331102:S=AA-AfjYzbp50e2rVJ93ztCxBlo1V',
    'showNewNextAdvertisement': '-10',
    'PHPSESSID': 'eyJ3ZWJTZXNzaW9uQXZhaWxhYmxlIjp0cnVlLCJ3ZWJQZXJzb25JZCI6MCwid2ViQ2xpZW50SWQiOjMwNzMyNzQ3NDUsIndlYkNsaWVudENvZGUiOjIxMTE5MDYxNzcsIndlYkNsaWVudENvb2tpZSI6ImI3MmU3Mzc5N2RlMTIxODEiLCJfZXhwaXJlIjoxNzA4NDE3NTA0MzAyLCJfbWF4QWdlIjo4NjQwMDAwMH0=',
    'PHPSESSID': '8CuKwSn-CMy_Q4ykZY9KPyC2RwsQozhx',
    '_gat': '1',
    '_dc_gtm_UA-110070444-1': '1',
    'FCNEC': '%5B%5B%22AKsRol9JB3LGJTKrlX3WbRwoYTHeTTzVDVpVQzmrVVmzDAf4ygfQzmO1qaIBJN3bkwxJie-QsAJAuKgEbg_hUyKZEeHhL1L4lTv-CBT2DFkf59YVVxbfOGCABnzntVI2dBb1IWEahOqbahcQO-ctPBT4ygPHdppHtw%3D%3D%22%5D%5D',
    'g_state': '{"i_p":1708338953805,"i_l":1}',
    'gdpr': '[2,3]',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://auto.ria.com/uk/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    # 'Cookie': 'Path=/; Path=/; chk=1; _ga=GA1.2.2134112153.1708331097; _gid=GA1.2.88012537.1708331097; test_new_features=810; ab-link-video-stories=2; news_prior=%7B%22item0%22%3A5%2C%22item1%22%3A4%2C%22item2%22%3A3%2C%22item3%22%3A2%7D; test_fast_search=1; _ga_KGL740D7XD=GS1.1.1708331097.1.1.1708331767.19.0.716172175; _gcl_au=1.1.1964028256.1708331097; AMP_TOKEN=%24NOT_FOUND; ui=b72e73797de12181; _504c2=http://10.42.5.231:3000; _fbp=fb.1.1708331098842.1685686992; __utma=79960839.2134112153.1708331097.1708331101.1708331101.1; __utmb=79960839.4.10.1708331101; __utmc=79960839; __utmz=79960839.1708331101.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); advanced_search_test=42; showNewFeatures=7; __gads=ID=0074f90a0ea9bc02:T=1708331102:RT=1708331102:S=ALNI_MZzLV9yrS_4mNN7Qn4_QFoKJGJ4tA; __gpi=UID=00000d5c64ac15e7:T=1708331102:RT=1708331102:S=ALNI_MZ0ROSeRx6OAmQDcUeHMSiz_CT_Kg; __eoi=ID=6b2210d8bcb1e034:T=1708331102:RT=1708331102:S=AA-AfjYzbp50e2rVJ93ztCxBlo1V; showNewNextAdvertisement=-10; PHPSESSID=eyJ3ZWJTZXNzaW9uQXZhaWxhYmxlIjp0cnVlLCJ3ZWJQZXJzb25JZCI6MCwid2ViQ2xpZW50SWQiOjMwNzMyNzQ3NDUsIndlYkNsaWVudENvZGUiOjIxMTE5MDYxNzcsIndlYkNsaWVudENvb2tpZSI6ImI3MmU3Mzc5N2RlMTIxODEiLCJfZXhwaXJlIjoxNzA4NDE3NTA0MzAyLCJfbWF4QWdlIjo4NjQwMDAwMH0=; PHPSESSID=8CuKwSn-CMy_Q4ykZY9KPyC2RwsQozhx; _gat=1; _dc_gtm_UA-110070444-1=1; FCNEC=%5B%5B%22AKsRol9JB3LGJTKrlX3WbRwoYTHeTTzVDVpVQzmrVVmzDAf4ygfQzmO1qaIBJN3bkwxJie-QsAJAuKgEbg_hUyKZEeHhL1L4lTv-CBT2DFkf59YVVxbfOGCABnzntVI2dBb1IWEahOqbahcQO-ctPBT4ygPHdppHtw%3D%3D%22%5D%5D; g_state={"i_p":1708338953805,"i_l":1}; gdpr=[2,3]',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

lk = []

start = 1

stop = 0

offset = 100

un = 0

url_template = 'https://auto.ria.com/uk/legkovie/?page=1'


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_json(session, url):
    async with session.get(url) as response:
        return await response.json()
    
async def take_link(start, offset, url_template, lk):
    idx = 0
    tasks = []
    links_processed = 0
    async with aiohttp.ClientSession() as session:
        for i in range(start, offset, 1):
            all_idx = (offset - start) * 10
            progress_step = 100 / all_idx
            
            url = url_template.replace("page=1", f"page={i}")
            tasks.append(fetch(session, url))
            links_processed += 1 
            print(f'links_processed  --- {links_processed} - of - {offset}')
        links_processed = 0 

        responses = await asyncio.gather(*tasks)
        for response_text in responses:
            soup = BeautifulSoup(response_text, 'lxml')
            data = soup.find_all('div', class_='item ticket-title')
            for a in data:
                link = a.find('a').get('href')
                lk.append(link)
                idx += 1
                progress_value = int(progress_step * idx)

                links_processed += 1 
                print(f'links_processed  --- {links_processed} - of - {offset * 10}')
            
async def main(un, start, stop, offset, url_template, lk):
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS phonebook (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, number TEXT)')
    await take_link(start, offset, url_template, lk)

    print(f'{len(lk)} links collected')
    all_iter = len(lk) if stop == 0 else stop
    progress_step = 100 / all_iter
    
    tasks = []
    async with aiohttp.ClientSession() as session:
        for link in lk:
            tasks.append(fetch(session, link))

        responses = await asyncio.gather(*tasks)
        for response_text in responses:
            soup = BeautifulSoup(response_text, 'lxml')
            script_tags = soup.select('script[class^="js-user-secure-"]')
            

            for script_tag in script_tags:
                data_hash = script_tag['data-hash']
                data_expire = script_tag['data-expires']
                order_id = soup.body['data-auto-id']
                response = await fetch_json(session, f'https://auto.ria.com/users/phones/{order_id}?hash={data_hash}&expires={data_expire}')

                title = 'Я'
                number = response['formattedPhoneNumber']
                
                number = re.sub('[^0-9]', '', number)  
                cursor.execute('SELECT * FROM phonebook WHERE number=?', (number,))
                result = cursor.fetchone()
                if not result:
                    cursor.execute('INSERT INTO phonebook (title, number) VALUES (?, ?)', (title, number))
                    conn.commit()

                    un += 1

                    print(f"{response['formattedPhoneNumber']} ( uniqu )  --- {un}")
                    with open('contacts_1.vcf', 'a', encoding='utf-8') as f:       
                        f.write(f'BEGIN:VCARD\nVERSION:3.0\nN:{title}\nTEL;TYPE=CELL:{number}\nEND:VCARD\n')
                    progress_value = int(progress_step * un)
                    if stop != 0 and un == stop:
                        return 0
                else:
                    un += 1
                    print(f"{response['formattedPhoneNumber']} ( NOT-uniqu )  --- {un}")

    print(f'{un} numbers processed')
    


time_start = time.time()
print(time_start)
asyncio.run(main(un, start, stop, offset, url_template, lk))

time_end = time.time()

print(f'Время выполнения --- {(time_end - time_start) / 60}')
