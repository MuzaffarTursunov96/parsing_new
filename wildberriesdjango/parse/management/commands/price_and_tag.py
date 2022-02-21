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
                
                with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\price.json", 'w',encoding='utf-8') as file:
                            json.dump(price1, file, indent=4, ensure_ascii=False)


tag_list=[]
               
class Command(BaseCommand):
    help='Parsing Wildberries'
    def handle(self, *args, **options):
        p=WildberiesParser()
        # p.get_dict('','https://www.wildberries.ru/catalog/elektronika/planshety',60,'Телефон стационарный',tag_list)
        p.get_dict_d('Крупная бытовая техника', 'https://www.wildberries.ru/catalog/bytovaya-tehnika/krupnaya-bytovaya-tehnika', 20,tag_list)