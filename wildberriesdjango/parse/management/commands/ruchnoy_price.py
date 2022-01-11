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

    def prod_papka_yaratish(self,cate_name, nomi):
        absolute_path = os.path.abspath(__file__)
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{cate_name}\{nomi}'):
            return True
        else:
            return False

    def remove_space(self,input_string):
        no_white_space = ''
        for c in input_string:
            if not c.isspace():
                no_white_space += c
        return no_white_space

    def change_price(self,name2,number2):
        absolute_path = os.path.abspath(__file__)
        for i in range(1, number2+1):
            with open(f"{os.path.dirname(absolute_path)}\{name2}\{i}.html", encoding='utf-8') as file:
                source = file.read()
            self.put_elements_ccc(source,name2,i)
    

    def put_elements_ccc(self, source, category_name,son):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)

        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            if not os.path.isdir(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}"):
                continue

            if not (os.path.exists(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\\brand.json") and os.path.getsize(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\\brand.json") != 0):
                continue
            
            if not os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\model.json"):
                continue
            
            print(papka)
            try:
                price1=product_hrefs.find(class_='lower-price').get_text()
            except AttributeError as ex:
                try:
                    price1=product_hrefs.find(class_='price-commission__current-price').get_text()
                except AttributeError as ex:
                    price1=product_hrefs.find(class_='price-commission__price').get_text()
            print(f'sahifa -============================={son}======================')
            price=self.remove_space(price1).replace('₽','')
            #price_commission__current-price
            print(f'{int(price)}')
            # if Elements.objects.filter(barcode=papka).exists():
            #     for elem_price in Elements.objects.filter(barcode=papka).all():
            #         Elements.objects.filter(id=elem_price.id).update(earn_point=int(price))

            if Variations.objects.filter(partnum=papka).exists():
                for var_price in Variations.objects.filter(partnum=papka).all():
                    Variations.objects.filter(id=var_price.id).update(prices=price)
            
            if Products.objects.filter(barcode=papka).exists():
                for pro_price in Products.objects.filter(barcode=papka).all():
                    Products.objects.filter(id=pro_price.id).update(price=price)
                    # print(pro_price.name)


    
            




class Command(BaseCommand):
    help='Parsing Wildberries'
    def handle(self, *args, **options):
        p=WildberiesParser()
        p.change_price('Стационарные телефоны', 3)







