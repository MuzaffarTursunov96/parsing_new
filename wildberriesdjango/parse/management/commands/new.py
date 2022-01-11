import random
from requests.exceptions import ConnectionError
import time
from collections import namedtuple
from bs4 import  BeautifulSoup
import  requests

import ast
import os
from http.client import IncompleteRead
import json



class Parse_text:
    def get_path3(self,cate_name,number,tag_list):
        absolute_path = os.path.abspath(__file__)
        for category_name, category_href in cate_name.items():
            for i in range(1, number+1):
                with open(f"{os.path.dirname(absolute_path)}\{category_name}\{i}.html", encoding='utf-8') as file:
                    source = file.read()
                print(i)    
                # self.product_characters(source, category_name)
                self.get_slug(source, category_name,tag_list)
    
    def product_characters(self,source, category_name):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            try:
                with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\product_detail.html", encoding='utf-8') as file:
                    soup = file.read()
            except FileNotFoundError as ex:
                continue
            # print(papka)
            source = BeautifulSoup(soup, 'lxml')
            try:
                caption = source.find(class_='product-params').find(class_='product-params__table').find('caption')
            except AttributeError as ex:
                pass
            
            if f'{papka}' =='36447857':
                continue
            if f'{papka}' =='34947460':
                continue
            if f'{papka}' =='30323097':
                continue
            if f'{papka}' =='13880664':
                continue
            if f'{papka}' =='19436095':
                continue
            if f'{papka}' =='19088798':
                continue
            print(papka)
            # print(source.find(class_='same-part-kt__color').find('span'))
            try:
                if source.find(class_='same-part-kt__color').find('span') !=None:
                    colo = source.find(class_='same-part-kt__color').find('span').get_text()
                    color=colo.replace(',','-')
                else:
                    color=''
            except AttributeError as ex:
                continue
            caption_name = 'Общие характеристики'
            cap_dict = {}
            sub_cap_dict = {}

            if source.find(class_='same-part-kt__common-info').find_all('p')[1:2] !=None:
                stars = source.find(class_='same-part-kt__common-info').find_all('p')[1:2]
                star_value = stars[0].find('span').get_text()
            else:
                star_value = source.find(class_='same-part-kt__common-info').find('a').find('span').find('span').getText()
            
           
            
            
            model_dict={}
            d_dict={}
            memory={}

            if caption != None:
                for a in caption.next_siblings:
                    if a.name == 'caption':
                        cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'
                        caption_name = a.get_text()
                        sub_cap_dict={}
                    else:
                        if a.find('tr') != -1 and a.find('tr') != None:
                            sub_name = a.find('tr').find('th').find('span').find('span').get_text()
                            sub_val = a.find('tr').find('td').get_text()
                            if sub_name =='Модель':
                                name = 'model'
                                model_dict[f'{sub_name}']=f'{sub_val}'
                                with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json", 'w',
                                            encoding='utf-8') as file:
                                    json.dump(model_dict, file, indent=4, ensure_ascii=False)
                            if sub_name == 'Диагональ экрана':
                                name = 'diagonal'
                                memory[f'{sub_name}'] = f'{sub_val}'
                                with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json", 'w',
                                            encoding='utf-8') as file:
                                    json.dump(memory, file, indent=4, ensure_ascii=False)

                            if sub_name =='Объем встроенной памяти (Гб)':
                                name = 'memory'
                                memory[f'{sub_name}']=f'{sub_val}'
                                with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json", 'w',
                                            encoding='utf-8') as file:
                                    json.dump(memory, file, indent=4, ensure_ascii=False)
                            sub_value = sub_val.split(';')
                            sub_cap_dict[f'{sub_name}'] = f'{sub_value}'
                        else:
                            continue
           
                cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'
                
            else:
                for a in source.find(class_='product-params').find(class_='product-params__table').find_all('tbody'):
                    sub_name = a.find('tr').find('th').find('span').find('span').get_text()
                    sub_val = a.find('tr').find('td').get_text()
                    if sub_name == 'Модель':
                        name = 'model'
                        model_dict[f'{sub_name}'] = f'{sub_val}'
                        with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json", 'w',
                                    encoding='utf-8') as file:
                            json.dump(model_dict, file, indent=4, ensure_ascii=False)

                    if sub_name == 'Объем встроенной памяти (Гб)':
                        name = 'memory'
                        memory[f'{sub_name}'] = f'{sub_val}'
                        with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json", 'w',
                                    encoding='utf-8') as file:
                            json.dump(memory, file, indent=4, ensure_ascii=False)
                    
                    if sub_name == 'Диагональ экрана':
                        name = 'diagonal'
                        memory[f'{sub_name}'] = f'{sub_val}'
                        with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json", 'w',
                                    encoding='utf-8') as file:
                            json.dump(memory, file, indent=4, ensure_ascii=False)

                    sub_value = sub_val.split(';')
                    sub_cap_dict[f'{sub_name}'] = f'{sub_value}'
                cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'
            
            descrip={}
            for desc in source.find_all(class_='product-detail__details details'):
                description_title = desc.find('h2').get_text()
                description_text = desc.find(class_='details__content').find('p').get_text()
                descrip[f'{description_title}'] = f'{description_text}'
            descrip['stars'] = f'{star_value}'
            descrip['color'] = f'{color}'
            with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\description.json", 'w', encoding='utf-8') as file:
                json.dump(descrip, file, indent=4, ensure_ascii=False)
            
            with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\product_characters.json", 'w', encoding='utf-8') as file:
                json.dump(cap_dict, file, indent=4, ensure_ascii=False)
    
    def get_slug(self,source, category_name,tag_list,categ_single='Ноутбук'):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            absolute_path = os.path.abspath(__file__)
            papka = self.nom(product_href)
            print(papka)
            if f'{papka}' =='36447857':
                continue
            if f'{papka}' =='34947460':
                continue
            if f'{papka}' =='30323097':
                continue
            product_brand=product_hrefs.find(class_='brand-name').getText()
            product_name=product_hrefs.find(class_='goods-name').getText()
            obsh=product_brand+' '+product_name
            categor_name = 'category'

            with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{categor_name}.json", 'w',
                      encoding='utf-8') as file:
                json.dump(categ_single, file, indent=4, ensure_ascii=False)

            # tag_name='extra_name'
            # for tag in tag_list:
            #     if tag in obsh:
            #         with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{tag_name}.json", 'w',encoding='utf-8') as file:
            #             json.dump(tag, file, indent=4, ensure_ascii=False)
                    
                

    
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
    
    def check_img_dir(self,category_name, papka, images):
        absolute_path = os.path.abspath(__file__)
        if os.path.isdir(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\{images}'):
            return True
        else:
            return False
    
    def get_html(self,url):
        response = self.test_request(url)
        if 'Requests quota exceeded' in response.text:
            time.sleep(60)
            return self.get_html(url)
        return response


tag_list=[
'DVD-плеер',
'Видеодиск',
'Диск для записи',
'Медиаплеер',
'Приемник видеосигнала'
]

if __name__ == "__main__":
    p=Parse_text()
    p.get_path3(cate_name={'Ноутбуки': 'https://www.wildberries.ru/catalog/elektronika/planshety'},number=6,tag_list=tag_list)