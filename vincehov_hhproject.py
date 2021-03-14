from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager # Обход PATH
import time # Время = деньги, как говорится
import sys, os  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets 
import design  # Файл дизайна
import re # Для отправки текста в форму входа
import urllib.parse # Чтобы закодировать текст в url 

def input_keys(phrase, input_form): # Единственный полезный кусок кода
    for key in re.findall(r'.', phrase): 
            time.sleep(0.1) # Каждый раз когда ты запускаешь прогу я убиваю len(phrase) * 0.1 секунд твоей жизни.
            input_form.send_keys(key)

def do_things(login, passwd, keyword_= None, reslink_= None):
    if "9773616899" in login: # Тут должно было идти диалоговое окошко "Настя, иди н!@#й", но мне лень 
        exit() 
        
    dr = webdriver.Chrome(ChromeDriverManager().install())
        # Инициализация
    count = 0 
    hrefs = []
    Moscow = False
    maximized = False
    refreshed = False 
    have_cookie = False 
    captha_solved = False 

    dr.get("https://hh.ru/account/login?backurl=%2F") # Вход в аккаунт
    time.sleep(1)

    login_form = dr.find_element_by_xpath("/html/body/div[6]/div/div[1]/div[3]/div/div/div/div/div/form/div[1]/input")
    password_form = dr.find_element_by_xpath("/html/body/div[6]/div/div[1]/div[3]/div/div/div/div/div/form/div[2]/span/input")

    input_keys(login, login_form) # Логин/Пароль
    input_keys(passwd, password_form)

    time.sleep(3)
    dr.find_element_by_xpath("/html/body/div[6]/div/div[1]/div[3]/div/div/div/div/div/form/div[4]/button").click()
    time.sleep(3)

    while captha_solved != True: # Проверка на то, решена ли капча
        try:
            captha = dr.find_element_by_class_name("bloko-form-error.bloko-form-error_entering")
            dr.execute_script("alert('Решите Капчу')")
            time.sleep(60)
        except:
            captha_solved = True
            pass
    try:
        dr.find_element_by_xpath("/html/body/div[2]/div/div/div/div[2]/div/div/form/div[4]/button").click()
    except:
           pass
    time.sleep(3)

    if reslink_:
        search = "https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&resume=%s&page=" % reslink_.split("https://hh.ru/resume/")[1]
    elif keyword_:
        search = "https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=%s&page=" % urllib.parse.quote(keyword_, safe='')
    else:
        search = "https://hh.ru/search/vacancy?L_is_autosearch=false&clusters=true&enable_snippets=true&text=python&page="

    while count < 12: # Выгребаем 600 вакансий
        
        dr.get("%s%d" % (search, count))
        count += 1 
        if not maximized:
            dr.maximize_window() 
            maximized = True
        bs = BeautifulSoup(dr.page_source,"lxml") 
        if not refreshed:
            dr.refresh()
        time.sleep(3)
        appended = 0
        for elem in  dr.find_elements_by_link_text('Откликнуться'):
            appended +=1 
            hrefs.append(elem.get_attribute("href"))
        if appended == 0:
            break
    
    
    badhrefs = []
    for orderhref in hrefs: # Откликаемся на вакансии
        try:
            dr.get(orderhref)
            dr.execute_script('document.getElementsByClassName("bloko-button                            bloko-button_primary                            HH-VacancyResponsePopup-Submit                            HH-SubmitDisabler-Submit                            HH-SimpleValidation-Submit")[0].click()')
        except:
            badhrefs.append(orderhref) # Это для отладки было сделано, осталось чисто по приколу
            pass
    
class ExampleApp(QtWidgets.QMainWindow, design.Ui_Dialog):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.initialize_text)
       
    def initialize_text(self):
        login_  = self.input_log.text()
        passwd_ = self.input_pass.text()
        keyword_ = self.input_keyword.text()
        reslink_ = self.input_reslink.text()
        self.close()
        do_things(login_, passwd_, keyword_, reslink_)

        
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  
