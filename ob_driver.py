from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
import colorama
from colorama import Fore, Back, Style
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class obWD:
    def init(self):
        lc_link = r'https://optom-brend.ru/moskva/zhenskaya-odezhda-optom/erotic-kostum'
        print(Fore.RED + 'Chrome Web Driver '+Fore.YELLOW +lc_link+Fore.RESET)
        chrome_options = webdriver.ChromeOptions()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        #chrome_prefs["profile.default_content_settings"] = {"images": 2}
        #chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--disable-notifications")
        #chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
        self.driver.maximize_window()
        self.Get_HTML(lc_link)
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[contains(@class,'js-log-form-active')]").click()
        time.sleep(1)
        #print(self.driver.find_element_by_name("email"))
        self.driver.find_element_by_name("email").send_keys("Lessie-May@yandex.ru")
        self.driver.find_element_by_name("password").send_keys("uslm1976")
        time.sleep(1)
        self.driver.find_element_by_xpath("//*[contains(@class,'js-log-form-submit')]").click()
        time.sleep(4)
        #self.driver.find_element_by_name("login").send_keys("Lessie")
        #self.driver.find_element_by_name("pass").send_keys("uslm1976")
        #self.driver.find_element_by_class_name("button").click()
        #self.driver.find_element_by_xpath("//input[contains(@value,'Войти')]").click()
    def __init__(self):
        self.init()

    def __del__(self):
        try:
            self.driver.quit()
            pass
        except: pass

    def Get_HTML(self, curl):
        self.driver.get(curl)
        return self.driver.page_source

    def Get_List_Of_Links_On_Goods_From_Catalog(self, curl):
        print(Fore.RED + 'Список товаров каталога: ' + Fore.YELLOW + curl + Fore.RESET)
        lst = []
        ls_links_pages_of_catalog = self.Get_List_Pages_Of_Catalog(curl)
        print('==========================', ls_links_pages_of_catalog)
        for link_on_page_of_catalog in ls_links_pages_of_catalog:
            print(Fore.YELLOW + 'Страницы каталога и товары на них: ' + Fore.LIGHTYELLOW_EX + link_on_page_of_catalog + Fore.RESET)
            print('Переходим: ', link_on_page_of_catalog)
            self.Get_HTML(link_on_page_of_catalog)
            elements = self.driver.find_elements(by=By.CLASS_NAME, value='product-item__content')
            for element in elements:
                lc_link = sx(element.get_attribute('innerHTML'), '<a href="','"')
                if lc_link not in lst:
                    lst.append(lc_link)
        return lst

    def Get_Link_On_Next_Catalog_Page(self):
        lc_link = ''
        try:
                lc_link = self.driver.find_element_by_xpath("//*[contains(@class,'tx_next fa fa-chevron-right')]").get_attribute('href')
        except: pass
        return lc_link

    def Get_List_Pages_Of_Catalog(self, c_link_on_first_catalog):
        lc_link_first = c_link_on_first_catalog
        ls_link_on_first_catalog = []
        lc_link_on_next_page = c_link_on_first_catalog
        while len(lc_link_on_next_page) > 5:
            print(Fore.YELLOW + 'Страницы каталога: ' + Fore.LIGHTYELLOW_EX + lc_link_on_next_page + Fore.RESET)
            if lc_link_on_next_page not in ls_link_on_first_catalog:
                ls_link_on_first_catalog.append(lc_link_on_next_page)
            else: break
            self.Get_HTML(lc_link_on_next_page)
            lc_link_on_next_page = self.Get_Link_On_Next_Catalog_Page()
        return ls_link_on_first_catalog

    def Write_To_File(self, cfilename):
        file = open(cfilename, "w", encoding='utf-8')
        file.write(self.driver.page_source)
        file.close()


def LoginOB():
    try:
        wd = obWD()
        print(1)
    except:
        try:
            wd = obWD()
            print(2)
        except:
            try:
                wd = obWD()
                print(3)
            except:
                try:
                    wd = obWD()
                    print(4)
                except:
                    pass
    return wd
#    if wd.driver.page_source.count('user773')>0:
#        print('Авторизация прошла успешно')
#        return wd
#    else:
#        print('Авторизация не прошла')
#        try:
#            pass
#            wd.driver.quit()
#        except:
#            print('Рекурсивный перезапуск')
#            return LoginOB()