import requests
from bs4 import BeautifulSoup
import lxml
import time
import sqlite3
import re
import asyncio
import aiohttp



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
