import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from multiprocessing import Pool







# Задаём параметры для браузера
options = Options()
options.add_argument("--disable-notifications")
options.add_argument("--disable-infobars")
options.add_argument("--mute-audio")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

# Указываем путь к драйверу Chrome
s = Service('./chromedriver.exe')

# Создаём экземпляр драйвера
driver = webdriver.Chrome(service=s, options=options)
driver.maximize_window()

# Проходим по страницам и сохраняем данные
def take_link():
    for i in range(0, 2, 1):
        
        url = f'https://auto.ria.com/uk/car/tesla/model-s/?page={i}'

        driver.get(url)
        
        html = driver.page_source

        soup = BeautifulSoup(html, 'lxml')
        data = soup.find_all('div', class_='item ticket-title')

        for a in data:
            link = a.find('a').get('href')
            yield link
with open('contacts.vcf', 'a', encoding='utf-8') as f:       
    for link in take_link():
        driver.get(link)
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        driver.execute_script("window.scrollBy(0, 450);")
        time.sleep(1)
        wait = WebDriverWait(driver, 10)
        # Находим элемент кнопки
        try:
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.phone.bold')))

            # Нажимаем на кнопку
            element.click()

            time.sleep(1)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')

            
            block = soup.find('div', class_ = 'popup-show-phone modal fade in')

            title = block.find('span', class_='i-block').text
            
            number = block.find('div', class_='popup-successful-call-desk').text
            
           
        except:
            print('Не удалось нажать на кнопку, пропускаем страницу')
            continue

        
        
     





# Закрываем браузер
driver.quit()
        
    