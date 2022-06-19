from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import sqlite3
from os import system
from my_library import *
import sys
from ob_driver import *
from ob_good import *
import colorama
from colorama import Fore, Back, Style

def unload_one_good(lc_link_on_good: str):
    print(Fore.YELLOW + 'Товар: ' + Fore.BLACK + Back.LIGHTWHITE_EX + lc_link_on_good + Fore.RESET + Back.RESET)
    lo_good = ob_good(lc_link_on_good)
    print(Fore.YELLOW + "Артикул: " + Fore.LIGHTGREEN_EX, lo_good.article, Fore.RESET)
    print(Fore.YELLOW + "Название:" + Fore.LIGHTGREEN_EX, lo_good.name, Fore.RESET)
    print(Fore.YELLOW + "Размеры:" + Fore.LIGHTGREEN_EX, lo_good.size_list, Fore.RESET)
    print(Fore.YELLOW + "Цена:" + Fore.LIGHTGREEN_EX, lo_good.price, Fore.RESET)
    print(Fore.YELLOW + "Цены:" + Fore.LIGHTGREEN_EX, lo_good.prices, Fore.RESET)
    print(Fore.YELLOW + "Цвета:" + Fore.LIGHTGREEN_EX, lo_good.colors, Fore.RESET)
    print(Fore.YELLOW + "Описание:" + Fore.LIGHTGREEN_EX, lo_good.description, Fore.RESET)
    print(Fore.YELLOW + "Картинки:" + Fore.LIGHTGREEN_EX, lo_good.pictures, Fore.RESET)

def unload_catalog_bodo(lc_first_page_of_catalog:str, lc_filename:str):
        price = Price(lc_filename+'.csv')
        pass
        lo_bodo = obWD()
        ll_list_links_on_goods = lo_bodo.Get_List_Of_Links_On_Goods_From_Catalog(lc_first_page_of_catalog)
        for g in ll_list_links_on_goods:
            if is_price_have_link(lc_filename + '.csv', g):
                print(Fore.LIGHTRED_EX, 'Товар уже имеется в прайсе:', Fore.YELLOW, g, Fore.RESET)
                continue
            try: lo_good = ob_good(lo_bodo, g)
            except:
                try:
                    lo_bodo = obWD()
                    lo_good = ob_good(lo_bodo, g)
                except:
                    lo_bodo = obWD()
                    lo_good = ob_good(lo_bodo, g)
            if len(lo_good.size) > 0:


                price.add_good('',
                               prepare_str(lo_good.article).strip() + ' ' + prepare_str(lo_good.name).strip(),
                               prepare_str(lo_good.description),
                               prepare_str(lo_good.price).replace(',', '.'),
                               '15',
                               prepare_str(g),
                               prepare_for_csv_non_list(lo_good.pictures),
                               prepare_for_csv_list(lo_good.size)
                               )
                price.write_to_csv(lc_filename + '.csv')
        lo_bodo.driver.quit()


def isnt_empty(p_param):
    #print(p_param)
    #lb_result = False
    if p_param == None:
     #   print('None')
        lb_result = False
    if type(p_param) == str:
     #   print('String')
        if len(p_param) > 0:
           lb_result = True
        else:
           lb_result = False
    if type(p_param) == int or type(p_param) == float:
      #  print('Number')
        if p_param != 0:
           lb_result = True
        else:
           lb_result = False
    #print(type(p_param), '->', p_param)
    return lb_result

def get_field_from_db_by_article_and_color(pc_article:str, pc_color:str, pc_field_name:str): # возвращает по переданному артикулу значение переданного поля, возвразает последнюю запись с нужным артикулом из таблицы
    pc_color = sx('|'+pc_color, '|', ',').replace("|","").strip()
    lc_sql_text = "select " + pc_field_name + " as value from bodo where rowid in (select max(rowid) from bodo where article = '" + pc_article + "' and color = '"+pc_color+"');"
    lo_result = cursor.execute(lc_sql_text).fetchone()
    if lo_result != None and lo_result[0]!=None:
        #print('артикул и цвет')
        return lo_result[0]
    else:
        #lc_sql_text = "select group_concat(" + pc_field_name + ", ' ') as value from bodo where  article = '" + pc_article + "';"
        lc_sql_text = "select " + pc_field_name + " as value from bodo where rowid in (select max(rowid) from bodo where article = '" + pc_article + "');"
        lo_result = cursor.execute(lc_sql_text).fetchone()
        if lo_result != None and lo_result[0]!=None:
            #print('артикул')
            return lo_result[0]
        else:
            lc_sql_text = "select " + pc_field_name + " as value from bodo where rowid in (select max(rowid) from bodo where instr(name, '" + pc_article + "')>0);"
            lo_result = cursor.execute(lc_sql_text).fetchone()
            if lo_result != None and lo_result[0]!=None:
                #print('артикул в названии')
                return lo_result[0]
            else: return ''


def save_good(price, pc_acticle, pc_name, pc_description, pc_price, ps_colors, pc_color):
    #lc_good = bodo_good(pc_acticle)
    #ls_pictures =lc_good.pictures
    lc_pictures = get_field_from_db_by_article_and_color(pc_acticle, pc_color, "pictures")
    print(Fore.YELLOW + 'Товар: ' + Fore.BLACK + Back.LIGHTWHITE_EX + pc_name + Fore.RESET + Back.RESET)
    print(Fore.YELLOW + "Размеры:" + Fore.LIGHTGREEN_EX, ps_colors, Fore.RESET)
    print(Fore.YELLOW + "Цена:" + Fore.LIGHTGREEN_EX, pc_price, Fore.RESET)
    print(Fore.YELLOW + "Описание:" + Fore.LIGHTGREEN_EX, pc_description, Fore.RESET)
    print(Fore.YELLOW + "Картинки:" + Fore.LIGHTGREEN_EX, lc_pictures, Fore.RESET)
    price.add_good('',
                   prepare_str(pc_name).strip(),
                   prepare_str(pc_description),
                   prepare_str(str(pc_price)).replace(',', '.'),
                   '15',
                   prepare_str(''),
                   prepare_str(lc_pictures),
                   prepare_for_csv_list(ps_colors)
                   )
    price.write_to_csv(r'g:\bodo\csvs\price.csv')
    return
    if len(lc_pictures)>10:
        price.add_good('',
               prepare_str(pc_name).strip(),
               prepare_str(pc_description),
               prepare_str(str(pc_price)).replace(',', '.'),
               '15',
               prepare_str(''),
               prepare_str(lc_pictures),
               prepare_for_csv_list(ps_colors)
               )
        price.write_to_csv(r'g:\bodo\csvs\price.csv')
    else:
        price_nopictures.add_good('',
               prepare_str(pc_name).strip(),
               prepare_str(pc_description),
               prepare_str(str(pc_price)).replace(',', '.'),
               '15',
               prepare_str(''),
               prepare_str(lc_pictures),
               prepare_for_csv_list(ps_colors)
               )
        price_nopictures.write_to_csv(r'g:\bodo\csvs\price_nopictures.csv')

def Store_into_database(lc_article:str, lc_name:str, lc_description:str, lc_pictures:str, lc_link:str, lc_color:str):
    cursor.execute("INSERT INTO bodo (article,name,description,pictures,link,color) "+
                   "VALUES ('" + lc_article + "', '" + lc_name + "', '" + lc_description + "', '" + lc_pictures + "', '" + lc_link + "', '" + lc_color + "')")

def is_link_into_db(pc_link:str):   #вовзращает истину, если ссылка на этот товар уже есть в БД
    #lo_connect = sqlite3.connect(r"G:\loverepublic\database\loverepublic.sqlite")
    #lo_cursor = lo_connect.cursor()
    lo_result = cursor.execute("select * from bodo where link = '" + pc_link + "'").fetchone()
    return (lo_result != None)

def get_field_from_db_by_article(pc_article:str, pc_field_name:str): # возвращает по переданному артикулу значение переданного поля, возвразает последнюю запись с нужным артикулом из таблицы
    lo_connect = sqlite3.connect(r"G:\bodo\database\bodo.sqlite")
    lo_cursor = lo_connect.cursor()
    lo_result = lo_cursor.execute("select " + pc_field_name + " as value from bodo where rowid in (select max(rowid) from bodo where article = '" + pc_article + "');").fetchone()
    if lo_result != None:
        return lo_result[0]
    else:
        return ''



def csv_to_data(pc_csv_path:str):
    list = open(pc_csv_path, 'r').read().splitlines()
    i = 0
    ln_imported_counter = 0
    for element in list:
        i = i + 1
        if i == 1:
            continue
        lsc = element
        lsc = lsc.replace('"', '')
        ll = lsc.split(';')
        lc_article = sx(' '+ll[1]+' ', ' ', ' ').strip()
        lc_name = ll[1].replace(lc_article, '').strip()
        lc_description = ll[2]
        lc_pictures = ll[6]
        lc_color = sx(' '+ll[7], ' ', ', ').strip()
        if get_field_from_db_by_article(lc_article,'pictures') == '':
            print('--------------------------------------------------------')
            print('Артикул: ', lc_article)
            print('Наименование: ', lc_name)
            print("Описание: ", lc_description)
            print('Цвет: ', lc_color)
            print('Ссылки: ', lc_pictures)
            print('===============  Импортировано =====================')
            Store_into_database(lc_article, lc_name, lc_description, lc_pictures, '', lc_color)
            ln_imported_counter = ln_imported_counter + 1
        else:
            print('===============  Пропуск товара, уже есть в БД =====================')
    print('Всего импортировано:', ln_imported_counter)




########################################################################################################################
########################################################################################################################
colorama.init()
#conn = sqlite3.connect(r"g:\BODO\database\bodo.sqlite")
#cursor = conn.cursor()
########################################################################################################################
#print(get_field_from_db_by_article_and_color("14-21U", "серый (черный)", "pictures"))
#exit()
########################################################################################################################
# проверка скачивании ссылок на страницы каталога
#wd = bodoWD()
#print(wd.Get_List_Of_Links_On_Goods_From_Catalog('https://bodo.su/malyshi/'))

#print(wd.Get_List_Pages_Of_Catalog('https://optom-brend.ru/abakan/bodo'))

#print(wd.Get_List_Of_Links_On_Goods_From_Catalog('https://optom-brend.ru/abakan/bodo'))



if sys.argv[1] == 'good':
    wd = LoginOB()
    print(sys.argv[1])
    print(sys.argv[2])
    good = ob_good(wd, sys.argv[2])


if sys.argv[1] == 'dump':
    wd = LoginOB()
    links_list = wd.Get_List_Of_Links_On_Goods_From_Catalog(sys.argv[2])
    print('Список товаров:', links_list)
    ln_total = len(links_list)
    ln_counter = 0
    price = Price(sys.argv[3])
    price_in_stock = Price(sys.argv[3]+'in_stock.csv')
    for link in links_list:
        ln_counter = ln_counter + 1
        print('Товар: ', link, Fore.LIGHTWHITE_EX, ln_counter, '/', ln_total, Fore.RESET)
        if is_price_have_link(sys.argv[3], link) or is_price_have_link(sys.argv[3]+'in_stock.csv', link):
            print('Товар уже имеется в прайсе')
        try:
            lo_good = ob_good(wd, link)
        except: continue
        lc_name = lo_good.name if lo_good.name.count(lo_good.article) != 0 else lo_good.article + ' ' + lo_good.name
        ll_unique = list(set(lo_good.prices))
        print('Уникальные цены: ', ll_unique)
        if len(lo_good.prices) != len(lo_good.sizes):
            print('Несоответствие количества цен и количества товаров, пропуск.')
            continue
        for lc_uprice  in ll_unique:
            j = 0
            ll_sizes = []
            ll_prices = []
            for lc_price in lo_good.prices:
                if lo_good.prices[j] == lc_uprice:
                    try:
                        ll_sizes.append(lo_good.sizes[j])
                    except:pass
                    #ll_prices.append(lo_good.prices[j])
                j = j + 1
                print('Шаг: ', j)
            if lo_good.name.count(' - в наличии') == 0:
                price.add_good('',
                                   prepare_str(lc_name),
                                   prepare_str(lo_good.description),
                                   prepare_str( str(round(float(lc_uprice.replace(',', '.').replace(' ', ''))*float(sys.argv[4]), 2))),
                                   '15',
                                   prepare_str(''),
                                   prepare_for_csv_non_list(lo_good.pictures),
                                   prepare_for_csv_list(ll_sizes)
                                   )
                price.write_to_csv(sys.argv[3])
            else:
                price_in_stock.add_good('',
                               prepare_str(lc_name),
                               prepare_str(lo_good.description),
                               prepare_str( str(round(float(lc_uprice.replace(',', '.').replace(' ', ''))*float(sys.argv[4]), 2))),
                               '15',
                               prepare_str(''),
                               prepare_for_csv_non_list(lo_good.pictures),
                               prepare_for_csv_list(ll_sizes)
                               )
                price_in_stock.write_to_csv(sys.argv[3]+'in_stock.csv')

    reverse_csv_price(sys.argv[3]+'in_stock.csv')
    reverse_csv_price(sys.argv[3])
