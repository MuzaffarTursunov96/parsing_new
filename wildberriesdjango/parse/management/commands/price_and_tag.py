import random
import time
from collections import namedtuple
from bs4 import  BeautifulSoup
import  requests
import os
import socks
from difflib import SequenceMatcher
import ast
from slugify import slugify
import shutil
import json
from parse.models import AttributeCategory,AttributeTranslations,Attributes,BranchTranslations,Branches,BrandTranslations,Brands,Categories,CategoryTranslations,CharacteristicTranslations,Characteristics,ColorTranslations,Colors,ElementTranslations,Elements,Products,Uploads,VariationTranslations,Variations,BrandCategory
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import argon2, binascii
from django.db.models import Q


class WildberiesParser:
    def get_dict_d(self, name1,link,number1,tags):
        absolute_path = os.path.abspath(__file__)
        self.get_path_d(name1,number1,tags)
    

    def nom(self,product_href):
        l = ''
        for i in reversed(product_href[:-25]):
            if i != '/':
                l += i
            else:
                break
            s = ''
            for i in reversed(l):
                s += i
        return s
    
    def remove_space(self,input_string):
        no_white_space = ''
        for c in input_string:
            if not c.isspace():
                no_white_space += c
        return no_white_space

    def get_path_d(self,name2,number2,tag_list):
        absolute_path = os.path.abspath(__file__)
        for i in range(1, number2+1):
            print(f'#####################  {i} chi sahifa ##############################')
            with open(f"{os.path.dirname(absolute_path)}\{name2}\{i}.html", encoding='utf-8') as file:
                source = file.read()
            self.product_css_d(source,name2,tag_list)

    def product_css_d(self, source, name,tag_list):
            soup = BeautifulSoup(source, 'lxml')
            all_product = soup.find_all(class_='product-card j-card-item')
            for product_hrefs in all_product:
                product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
                papka = self.nom(product_href)
                absolute_path = os.path.abspath(__file__)
                product_brand = product_hrefs.find(class_='brand-name').getText()
                product_name = product_hrefs.find(class_='goods-name').getText()
                obsh = product_brand + ' ' + product_name

                if os.path.isdir(f'{os.path.dirname(absolute_path)}\{name}\{papka}'):
                    for tag in tag_list:
                        if tag in obsh:
                            with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\\extra_name_d.json", 'w',encoding='utf-8') as file:
                                json.dump(tag, file, indent=4, ensure_ascii=False)
                            break
                    try:
                        price1=product_hrefs.find(class_='lower-price').get_text()
                    except AttributeError as ex:
                        try:
                            price1=product_hrefs.find(class_='price-commission__current-price').get_text()
                        except AttributeError as ex:
                            price1=product_hrefs.find(class_='price-commission__price').get_text()
                    
                    price=self.remove_space(price1).replace('₽','')

                    with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\price.json", 'w',encoding='utf-8') as file:
                                json.dump(price, file, indent=4, ensure_ascii=False)


tag_list=[
'Аксессуар для аэрогриля',
'Аксессуар для мультиварки',
'Аксессуар для проращивателя семян',
'Аксессуар для тостера',
'Аксессуар для хлебопечки',
'Аксессуар для электрогриля',
'Аксессуары для мясорубок',
'Банка для йогуртницы',
'Дымогенератор для копчения',
'Запчасти для СВЧ',
'Запчасть для плиты',
'Картофелечистка электрическая',
'Льдогенератор',
'Насадка для блендера',
'Насадка для миксера',
'Ножи для мясорубок',
'Панель для мультипекаря',
'Переходник для плиты',
'Полка в холодильник',
'Прибор экологического контроля',
'Термометр для холодильника',
'Термощуп',
'Фильтр для вытяжки',
'Фильтр для фритюра',
'Чаша для мультиварки',
'Шестерня для мясорубки',
'Электрический консервный нож'

]
               
class Command(BaseCommand):
    help='Parsing Wildberries'
    def handle(self, *args, **options):
        p=WildberiesParser()
        # p.get_dict('','https://www.wildberries.ru/catalog/elektronika/planshety',60,'Телефон стационарный',tag_list)
        p.get_dict_d('Аксессуары для кухонной техники', 'https://www.wildberries.ru/catalog/bytovaya-tehnika/krupnaya-bytovaya-tehnika', 20,tag_list)