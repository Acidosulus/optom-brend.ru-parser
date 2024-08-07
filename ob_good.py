from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
from my_library import *
from ob_driver import *
import colorama
from colorama import Fore, Back, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib import request
from urllib.parse import quote

def poiskpers(url):
    geourl = '{0}'.format(quote(url))
    return geourl

class ob_good:
    def __init__(self, ol:obWD, lc_link):
        lc_link = lc_link.replace(r'amp;', '')
        self.pictures = []
        self.sizes = []
        self.prices = []
        self.color = ''
        self.article = ''
        self.name = ''
        self.description= ''
        self.price = ''
        self.brand = ''
        self.sale = False
        print(Fore.LIGHTGREEN_EX, 'Товар: ', Fore.LIGHTBLUE_EX, lc_link, Fore.RESET)
        self.source = ol.Get_HTML(lc_link)
        #ol.Write_To_File('good_debug.html')
        try: self.name = ol.driver.find_element(By.TAG_NAME, value = 'h1').text
        except: self.name = ''
        
        if ol.driver.page_source.count('class="product-old-price')>0:
            self.sale = True
        #"//*[contains(@class,'')]"
        #"//*[contains(@class,'')]"

        try: self.article = ol.driver.find_element(By.XPATH, value = "//*[contains(@class,'js-sku-pp')]").text
        except: self.article = ''

        try: self.brand = ol.driver.find_element(By.XPATH, value = "//*[contains(@class,'product-page__info__brand g-sm-t-14 g-bold')]").text
        except: self.brand = ''

        try: self.price = ol.driver.find_element(By.XPATH, value = "//*[contains(@class,'g-sm-t-26 g-t-pink')]").text.replace('р.','').replace(' ','')
        except: self.price = ''

        try: self.description = ol.driver.find_element(By.XPATH, value = "//*[contains(@class,'g-text')]").text.replace('\n','').replace('\r','')
        except: self.description = ''

        for i in range(0,ol.driver.page_source.count('<div class="slide g-al-center">')+1):
            picture = sx( sx(ol.driver.page_source,'<div class="slide g-al-center">', '</div>', i), '<a data-fancybox="gallery" href="', '">').replace(r'ru//', r'ru/').strip()
            picture = poiskpers(picture.replace('https://','')).replace(' ','').replace('//','/')
            picture = ('https://' if len(picture) else '') + picture
            print(i, '-', picture)
            picture = picture
            
            if picture not in self.pictures and len(picture)!=0 :
                self.pictures.append(picture)

        table = ol.driver.find_element(By.XPATH, value = "//*[contains(@class,'product-page-variants g-sm-1')]")
        lc_table = table.get_attribute('innerHTML')
        lc_left = '''<tr>
												<td>'''
        if lc_table.count(lc_left)>0:
            #  Pelican
            pass
        else:
            # visa-vis
            lc_left = '''<tr>
                          <td>'''
        for i in range(1, lc_table.count(lc_left)+1):
            lc_size = sx(lc_table, lc_left, '</td>', i).strip()
            lc_price = sx(lc_table, '<span class="g-t-pink">', '<', i).replace('Р', '').replace(' ', '').replace('р.', '')
            if lc_size not in self.sizes and len(lc_size)>0:
                self.sizes.append(lc_size)
                self.prices.append(lc_price)
            print(lc_size, ' <-====-> ', lc_price)




        elements = ol.driver.find_elements_by_xpath("//*[contains(@class,'name_tb')]")
        #print('Количество размеров:', len(elements))
        for element in elements:
            lc_size = element.text
            if lc_size not in self.sizes and lc_size != 'Наименование':
                self.sizes.append(lc_size)

        for i in range(0, ol.driver.page_source.count('/ <span class="g-t-red">')):
            self.prices.append(sx(ol.driver.page_source, '/ <span class="g-t-red">', '</span>', i+1).replace('р.', '').strip())

        print(Fore.LIGHTGREEN_EX, 'Артикул: ', Fore.LIGHTCYAN_EX, self.article, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Название: ', Fore.LIGHTCYAN_EX, self.name, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Бренд: ', Fore.LIGHTCYAN_EX, self.brand, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Цена: ', Fore.LIGHTCYAN_EX, self.price, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Картинки: ', Fore.LIGHTCYAN_EX, self.pictures, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Описание: ', Fore.LIGHTCYAN_EX, self.description, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Размеры: ', Fore.LIGHTCYAN_EX, self.sizes, Fore.RESET)
        print(Fore.LIGHTGREEN_EX, 'Цены: ', Fore.LIGHTCYAN_EX, self.prices, Fore.RESET)
