import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import re
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import sqlite3

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
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.pushButton.clicked.connect(self.on_pushButton_clicked)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AutoRia Parser"))
        self.pushButton.setText(_translate("MainWindow", "Старт"))
        self.label_num.setText(_translate("MainWindow", "Введите количество страниц:"))
        self.label_link.setText(_translate("MainWindow", "Введите ссылку:"))
        self.label_start.setText(_translate("MainWindow", "С какой страницы начать:"))
        self.label_stop.setText(_translate("MainWindow", "Сколько номеров записать:"))

    def on_pushButton_clicked(self):
        url_template = self.line_link.text()
        offset = int(self.line_num.text())
        start =int(self.line_start.text())
        stop = int(self.lineEdit.text())

        conn = sqlite3.connect('phonebook.db')
        cursor = conn.cursor()

        cursor.execute('CREATE TABLE IF NOT EXISTS phonebook (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, number TEXT)')

        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

        # Указываем путь к драйверу Chrome
        s = Service('./chromedriver.exe')
        num = 0
        # Создаём экземпляр драйвера
        driver = webdriver.Chrome(service=s, options=options)
        driver.maximize_window()

        # Проходим по страницам и сохраняем данные
        def take_link():
            for i in range(start, offset, 1):
                
                url = url_template.replace("page=1", f"page={i}")

                driver.get(url)
                
                html = driver.page_source

                soup = BeautifulSoup(html, 'lxml')
                data = soup.find_all('div', class_='item ticket-title')

                for a in data:
                    link = a.find('a').get('href')
                    yield link
        with open('contacts_1.vcf', 'a', encoding='utf-8') as f:       
            for link in take_link():
                driver.get(link)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                driver.execute_script("window.scrollBy(0, 450);")
                time.sleep(2)
                wait = WebDriverWait(driver, 10)
                # Находим элемент кнопки
                try:
                    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.phone.bold')))

                    # Нажимаем на кнопку
                    element.click()

                    time.sleep(3)
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'lxml')

                    
                    block = soup.find('div', class_ = 'popup-show-phone modal fade in')

                    title = 'Я'
                    
                    number = block.find('div', class_='popup-successful-call-desk').text
                    
                    if number:
                        number = re.sub('[^0-9]', '', number)  
                        cursor.execute('SELECT * FROM phonebook WHERE number=?', (number,))
                        result = cursor.fetchone()
                        if not result:
                            cursor.execute('INSERT INTO phonebook (title, number) VALUES (?, ?)', (title, number))
                            conn.commit()

                            print(title, number)
                            f.write(f'BEGIN:VCARD\nVERSION:3.0\nN:{title}\nTEL;TYPE=CELL:{number}\nEND:VCARD\n')
                            num += 1
                            if num == stop:
                                break
                except:
                    print('Не удалось нажать на кнопку, пропускаем страницу')
                    continue


        # Закрываем браузер
        driver.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())