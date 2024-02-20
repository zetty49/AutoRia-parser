from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import requests
from bs4 import BeautifulSoup
import lxml
import time
import sqlite3
import re
import sys
from threading import Thread


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

def take_link(start, offset, url_template, progress_bar):
    idx = 0
    for i in range(start, offset, 1):
        all_idx = (offset - start) * 10
        progress_step = 100 / all_idx
        
        url = url_template.replace("page=1", f"page={i}")

        time_start = time.time()
        response = requests.get(url=url, cookies=cookies, headers=headers)
        
        soup = BeautifulSoup(response.text, 'lxml')
        data = soup.find_all('div', class_='item ticket-title')

        for a in data:
            link = a.find('a').get('href')
            lk.append(link)
            idx +=1
            progress_value = int(progress_step * idx)
            
            progress_bar.setValue(progress_value)

def main(num, start, offset, stop, url_template, progress_bar, status, un):

    status.setText('Подготовка ссылок...')
    conn = sqlite3.connect('phonebook.db')
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS phonebook (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, number TEXT)')
    take_link(start, offset, url_template, progress_bar)

    print(f'{len(lk)} links collected')
    progress_bar.setValue(1)
    status.setText('Обработка ссылок...')
    all_iter = len(lk) if stop == 0 else stop
    progress_step = 100 / all_iter
    for link in lk:
        
        response = requests.get(url=link, cookies=cookies, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')

        script_tags = soup.select('script[class^="js-user-secure-"]')
        order_id = link.split('_')[-1].split('.')[0]
        
        for script_tag in script_tags:
            data_hash = script_tag['data-hash']
            data_expire = script_tag['data-expires']
            
            response = requests.get(url=f'https://auto.ria.com/users/phones/{order_id}?hash={data_hash}&expires={data_expire}', cookies=cookies, headers=headers)

            title = 'Я'
            number = response.json()['formattedPhoneNumber']
            
            
            number = re.sub('[^0-9]', '', number)  
            cursor.execute('SELECT * FROM phonebook WHERE number=?', (number,))
            result = cursor.fetchone()
            if not result:
                cursor.execute('INSERT INTO phonebook (title, number) VALUES (?, ?)', (title, number))
                conn.commit()

                un +=1
                
                print(f"{response.json()['formattedPhoneNumber']} ( uniqu )  --- {un}")
                with open('contacts_1.vcf', 'a', encoding='utf-8') as f:       
                    f.write(f'BEGIN:VCARD\nVERSION:3.0\nN:{title}\nTEL;TYPE=CELL:{number}\nEND:VCARD\n')
                progress_value = int(progress_step * un)
                progress_bar.setValue(progress_value)
                if stop != 0 and un == stop:
                    progress_bar.setValue(100)
                    status.setText(f'Сбор номеров завершен!  ---   записано {un} уникальных номеров')
                    return 0 
                    

            num += 1
            
            

    progress_bar.setValue(100)
    status.setText(f'Сбор номеров завершен!  ---   записано {un} уникальных номеров')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(290, 510, 231, 31))
        self.pushButton.setObjectName("pushButton")
        self.line_link = QtWidgets.QLineEdit(self.centralwidget)
        self.line_link.setGeometry(QtCore.QRect(10, 190, 681, 21))
        self.line_link.setText("")
        self.line_link.setObjectName("line_link")
        self.line_num = QtWidgets.QLineEdit(self.centralwidget)
        self.line_num.setGeometry(QtCore.QRect(10, 260, 201, 20))
        self.line_num.setText("")
        self.line_num.setObjectName("line_num")
        self.label_num = QtWidgets.QLabel(self.centralwidget)
        self.label_num.setGeometry(QtCore.QRect(10, 240, 171, 16))
        self.label_num.setObjectName("label_num")
        self.label_link = QtWidgets.QLabel(self.centralwidget)
        self.label_link.setGeometry(QtCore.QRect(10, 170, 161, 16))
        self.label_link.setObjectName("label_link")
        self.line_start = QtWidgets.QLineEdit(self.centralwidget)
        self.line_start.setGeometry(QtCore.QRect(10, 330, 201, 20))
        self.line_start.setObjectName("line_start")
        self.label_start = QtWidgets.QLabel(self.centralwidget)
        self.label_start.setGeometry(QtCore.QRect(10, 310, 161, 16))
        self.label_start.setObjectName("label_start")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 400, 201, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_stop = QtWidgets.QLabel(self.centralwidget)
        self.label_stop.setGeometry(QtCore.QRect(10, 380, 161, 16))
        self.label_stop.setObjectName("label_stop")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 440, 781, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(10, 470, 781, 20))
        self.status_label.setObjectName("status_label")
        self.status_label.setStyleSheet("color: green; background-color: black;")
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)  # Соединяем событие нажатия на кнопку с методом


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AutoRia Parser"))
        self.pushButton.setText(_translate("MainWindow", "Старт"))
        self.label_num.setText(_translate("MainWindow", "Введите количество страниц:"))
        self.label_link.setText(_translate("MainWindow", "Введите ссылку:"))
        self.label_start.setText(_translate("MainWindow", "С какой страницы начать:"))
        self.label_stop.setText(_translate("MainWindow", "Сколько номеров записать:"))
        self.status_label.setText(_translate("MainWindow", "Ожидание запуска..."))


    def on_pushButton_clicked(self):

        
        url_template = self.line_link.text()
        offset = int(self.line_num.text())
        start =int(self.line_start.text())
        stop = int(self.lineEdit.text())
        print('started')
        
        num = 0
        un = 0

        t = Thread(target=main, args=(num, start, offset, stop, url_template, self.progressBar, self.status_label, un))
        t.start()
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())