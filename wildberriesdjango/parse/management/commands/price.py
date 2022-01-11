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

    def read_file(self,path):
        file = open(path, "r",encoding='utf-8')
        data = file.read()
        file.close()
        return data

    def read_json(self,path):
        return json.loads(self.read_file(path))


    def remove_all_spaces(self,str):
        return "".join(str.strip())

    
    
    
    
    
    
    
    #_________ ################## ---------D------------#################______________
    def get_dict_d(self,num,num_product):
        absolute_path = os.path.abspath(__file__)
        categories_3_2 = self.read_json(f"{os.path.dirname(absolute_path)}\category_three.json")

        for name_id_1,dat in categories_3_2.items():
            for name_id_2, link in dat.items():
                self.get_path_d(num,name_id_1,name_id_2,num_product)

    
    def get_path_d(self,num,cate_11,cate_22,num_pro):
        absolute_path = os.path.abspath(__file__)
        for i in range(1, num+1):
            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{cate_11}\{cate_22}\{i}.html"):
                with open(f"{os.path.dirname(absolute_path)}\{cate_11}\{cate_22}\{i}.html", encoding='utf-8') as file:
                    source = file.read()
                soup = BeautifulSoup(source, 'lxml')
                all_product = soup.find_all(class_='product-card j-card-item')
                if all_product == None:
                    continue
                self.put_elements_d(source,cate_11,cate_22,num_pro)
    
    def put_elements_d(self, source, name11,name22,product_num):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        x=0
        for product_hrefs in all_product:
            if x==product_num:
                break
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            if not os.path.isdir(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}"):
                continue
            print(papka)
            
            mal=self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\description.json")
            color = mal['color']
            pro_name=self.remove_all_spaces(product_hrefs.find(class_='goods-name').getText())

            a=f'{pro_name}'
            dddd=f"{a}, {color}"
            if ((len(dddd)>255)):
                continue

            price1=product_hrefs.find(class_='lower-price').get_text()
            price=self.remove_space(price1).replace('₽','')
            # & Q(brand_id=brand_id)
            if Elements.objects.filter(Q(name=f"{a}") & Q(category_id=name11)).exists():
                if Elements.objects.filter(Q(name=f"{a}") & Q(category_id=name11) & Q(barcode=papka)).exists():
                    id=Elements.objects.filter(Q(name=f"{a}") & Q(category_id=name11)&Q(barcode=papka))[:1].get().id
                    Elements.objects.filter(id=id).update(earn_point=int(price))
                    if color!='':
                        var_a = a+', '+color
                    else:
                        var_a = a

                    Variations.objects.filter(name=var_a).update(prices=price)
                    pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                    for i in range(0, 3):
                        var_a1 = var_a + pro_names[i]
                        Products.objects.filter(name=var_a1).update(price=price)
            x+=1

    
    
    ################-------------D end----------###################
    
    
    
    
    
    def get_dict(self,num,num_product):
        absolute_path = os.path.abspath(__file__)
        categories_2 = self.read_json(f"{os.path.dirname(absolute_path)}\category_two.json")
        for name_id, link in categories_2.items():
            self.get_path_c(num,name_id,num_product)


    
    
    def get_path_c(self,num,cate_22,num_pro):
        absolute_path = os.path.abspath(__file__)
        for i in range(1, num+1):
            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{cate_22}\{i}.html"):
                with open(f"{os.path.dirname(absolute_path)}\{cate_22}\{i}.html", encoding='utf-8') as file:
                    source = file.read()
                soup = BeautifulSoup(source, 'lxml')
                all_product = soup.find_all(class_='product-card j-card-item')
                if all_product == None:
                    continue
                self.put_elements_c(source,cate_22,num_pro)
    
    def put_elements_c(self, source, name11,product_num):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        x=0
        for product_hrefs in all_product:
            if x==product_num:
                break
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            if not os.path.isdir(f"{os.path.dirname(absolute_path)}\{name11}\{papka}"):
                continue
            print(papka)
            
            mal=self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\description.json")
            color = mal['color']
            pro_name=self.remove_all_spaces(product_hrefs.find(class_='goods-name').getText())

            a=f'{pro_name}'
            dddd=f"{a}, {color}"
            if ((len(dddd)>255)):
                continue

            price1=product_hrefs.find(class_='lower-price').get_text()
            price=self.remove_space(price1).replace('₽','')
            # & Q(brand_id=brand_id)
            if Elements.objects.filter(Q(name=f"{a}") & Q(category_id=name11)).exists():
                if Elements.objects.filter(Q(name=f"{a}") & Q(category_id=name11) & Q(barcode=papka)).exists():
                    id=Elements.objects.filter(Q(name=f"{a}") & Q(category_id=name11)&Q(barcode=papka))[:1].get().id
                    Elements.objects.filter(id=id).update(earn_point=int(price))
                    if color!='':
                        var_a = a+', '+color
                    else:
                        var_a = a

                    Variations.objects.filter(name=var_a).update(prices=price)
                    pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                    for i in range(0, 3):
                        var_a1 = var_a + pro_names[i]
                        Products.objects.filter(name=var_a1).update(price=price)
            x+=1




class Command(BaseCommand):
    help='Parsing Wildberries'
    def handle(self, *args, **options):
        p=WildberiesParser()
        
        p.get_dict_d('Планшеты', 2)







