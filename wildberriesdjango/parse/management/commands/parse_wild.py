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
from jsondiff import diff
from django.core.exceptions import ObjectDoesNotExist
import argon2, binascii
from django.db.models import Q



class WildberiesParser:

    def test_request(self, url, retry=550):
        try:
            proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            useragents = [
                'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
                'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; Avant Browser)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                'Mozilla/4.0 (compatible; Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser 1.98.744; .NET CLR 3.5.30729); Windows NT 5.1; Trident/4.0)',
                'Mozilla/4.0 (compatible; Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727); Windows NT 5.1; Trident/4.0; Maxthon; .NET CLR 2.0.50727; .NET CLR 1.1.4322; InfoPath.2)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB6; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB6; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; GTB5; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; InfoPath.1; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Acoo Browser; InfoPath.2; .NET CLR 2.0.50727; Alexa Toolbar)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Acoo Browser; .NET CLR 2.0.50727; .NET CLR 1.1.4322)',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Acoo Browser; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727; FDM; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; InfoPath.2)',
                'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Acoo Browser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)'
            ]
            headers = {
                'User-Agent': f'{random.choices(useragents)}'
            }

            response = requests.get(url, headers=headers, proxies=proxies)

        except ConnectionError as ex:
            time.sleep(60)
            if retry:
                print(1)
                return self.test_request(url, retry={retry - 1})
            else:
                raise
        except socks.SOCKS5Error as ex:
            time.sleep(600)
            if retry:
                print(3)
                return self.test_request(url, retry={retry - 1})
            else:
                raise
        except:
            time.sleep(60)
            if retry:
                print(2)
                return self.test_request(url, retry={retry - 1})
            else:
                raise
        else:
            return response



    def check_exists(self,cate_name, prod_name):
        absolute_path = os.path.abspath(__file__)
        filees = os.path.isfile(f'{os.path.dirname(absolute_path)}\{cate_name}\{prod_name}\product_detail.html')
        return filees

    def get_slugify(self,name):
        return slugify(f'{name}', to_lower=True)


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


    def cut_model(self,names,brand,diagonal):
        print(f'1-----------{names}------brand={brand}')
        # names=names
        if diagonal !='':
            rep_list=[f'{brand.capitalize()}',f'{brand.lower()}','Wi-Fi','LTE','+',f'{diagonal}','Cellular']
        else:
            rep_list = [f'{brand.capitalize()}',f'{brand.lower()}','Wi-Fi', 'LTE', '+','Cellular']
        a = names
        for rep in rep_list:
            if f'{rep}' in names:
                a=names.replace(rep,'')
                names=a
        return names.split(';')[0]
        # print(f'2---------{a}')
        # if 'Gb' in names:
        #     gb_ind = names.index('Gb')
        #     h = ''
        #     for i in reversed(names[:gb_ind]):
        #         h += i
        #     pro_ind = h.index(' ')
        #     a = ''
        #     c = h[pro_ind:]
        #     for i in reversed(c):
        #         a += i
        # elif "TB" in names:
        #     gb_ind = names.index('TB')
        #     if names[gb_ind+2]==' ':
        #         h = ''
        #         for i in reversed(names[:gb_ind]):
        #             h += i
        #         pro_ind = h.index(' ')
        #         a = ''
        #         c = h[pro_ind:]
        #         for i in reversed(c):
        #             a += i
        #     else:
        #         return names
        # elif "GB" in names:
        #     gb_ind = names.index('GB')
        #     h = ''
        #     for i in reversed(names[:gb_ind]):
        #         h += i
        #     try:
        #         pro_ind = h.index(' ')
        #     except ValueError as ex:
        #         pro_ind=0
        #     a = ''
        #     c = h[pro_ind:]
        #     for i in reversed(c):
        #         a += i
        # elif "Tb" in names:
        #     gb_ind = names.index('Tb')
        #     h = ''
        #     for i in reversed(names[:gb_ind]):
        #         h += i
        #     pro_ind = h.index(' ')
        #     a = ''
        #     c = h[pro_ind:]
        #     for i in reversed(c):
        #         a += i
        # cy=a.split(';')[0]
        # return cy

    def check_img_dir(self,category_name, papka, images):
        absolute_path = os.path.abspath(__file__)
        if os.path.isdir(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\{images}'):
            return True
        else:
            return False
    def branch_translation(self,branch_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            p=BranchTranslations(
                branch_id=branch_id,
                name=name,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()

    def char_translation(self,char_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            p=CharacteristicTranslations(
                characteristic_id=char_id,
                name=name,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()

    def similar(self,a, b):
        return SequenceMatcher(None, a, b).ratio()

    def attribute_translation(self,atr_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            p=AttributeTranslations(
                attribute_id=atr_id,
                name=name,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()



    def brand_translation(self,brand_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            p=BrandTranslations(
                brand_id=brand_id,
                name=name,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()

    def color_translation(self,color_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            p=ColorTranslations(
                color_id=color_id,
                name=name,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()

    def var_translation(self,var_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            VariationTranslations(
                variation_id=var_id,
                name=name,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()
    def elem_translation(self,elem_id,name,des):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            ElementTranslations(
                element_id=elem_id,
                name=name,
                description=des,
                lang=lang,
                created_at='2021-05-21 02:19:37',
                updated_at='2021-05-21 02:19:37'
            ).save()


    #######################        Baza       #############################

    def get_attributes(self, name):
        attribute_id = Attributes.objects.filter(name=name)[:1].get().id
        return attribute_id

    def read_file(self,path):
        file = open(path, "r",encoding='utf-8')
        data = file.read()
        file.close()
        return data

    def remove_space(self,input_string):
        no_white_space = ''
        for c in input_string:
            if not c.isspace():
                no_white_space += c
        return no_white_space


    def hash_and_move(self,name,url):
        arr = bytes(name, 'utf-8')
        absolute_path = os.path.abspath(__file__)
        hash = argon2.hash_password_raw(time_cost=8, memory_cost=4096, parallelism=1, hash_len=12,
            password=arr, salt=b'muzaffar*96#', type=argon2.low_level.Type.ID)
        a = str(binascii.hexlify(hash))[2:-1]
        n='all'
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\\uploads'):
            parent_dir1 = f'{os.path.dirname(absolute_path)}'
            parent_dir2 = f'{os.path.dirname(absolute_path)}\\uploads'
            path1 = os.path.join(parent_dir1, f'uploads')
            path2 = os.path.join(parent_dir2, f'all')
            os.mkdir(path1)
            os.mkdir(path2)
        shutil.copy2(url,f'{os.path.dirname(absolute_path)}\\uploads\\{n}\\{a}.jpg')
        return a

    def remove_all_spaces(self,str):
        return "".join(str.strip())

    def cate_dir(self, name):
        absolute_path = os.path.abspath(__file__)
        parent_dir = f'{os.path.dirname(absolute_path)}'
        path = os.path.join(parent_dir, f'{name}')
        os.mkdir(path)

    def get_html(self, url):
        response = self.test_request(url)
        if 'Requests quota exceeded' in response.text:
            time.sleep(60)
            return self.get_html(url)
        return response

    def get_dict(self, name1,link,number1,extra,tag_list):
        absolute_path = os.path.abspath(__file__)
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name1}'):
            self.cate_dir(name1)
        for i in range(1,number1+1):
            if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{name1}\{i}.html'):
                response = self.get_html(f'{link}?page={i}')
                time.sleep(3)
                source = response.text
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{i}.html", 'w', encoding='utf-8') as file:
                    file.write(source)
        self.get_path_c(name1,number1,extra,tag_list)

    def get_path_c(self,name2,number2,extr,tags):
        absolute_path = os.path.abspath(__file__)
        for i in range(1, number2+1):
            with open(f"{os.path.dirname(absolute_path)}\{name2}\{i}.html", encoding='utf-8') as file:
                source = file.read()
            self.product_css_c(source,name2,tags)
            self.product_characters_cc(source,name2)
            self.product_attributes_c(source,name2)
            self.put_elements_c(source,name2,extr)


    def get_dict_d(self, name1,link,number1,tags):
        absolute_path = os.path.abspath(__file__)
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name1}'):
            self.cate_dir(name1)
        for i in range(1,number1+1):
            if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{name1}\{i}.html'):
                response = self.get_html(f'{link}?page={i}')
                time.sleep(3)
                source = response.text
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{i}.html", 'w', encoding='utf-8') as file:
                    file.write(source)
        self.get_path_d(name1,number1,tags)

    def get_path_d(self,name2,number2,tag_list):
        absolute_path = os.path.abspath(__file__)
        for i in range(1, number2+1):
            print(f'#####################  {i} chi sahifa ##############################')
            with open(f"{os.path.dirname(absolute_path)}\{name2}\{i}.html", encoding='utf-8') as file:
                source = file.read()
            self.product_css_d(source,name2,tag_list)
            self.product_characters_dd(source,name2)
            # self.product_attributes_d(source,name2)
            # self.put_elements_d(source,name2)

    def product_css_c(self, source, name,tag_list):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            print(papka)
            absolute_path = os.path.abspath(__file__)

            product_brand = product_hrefs.find(class_='brand-name').getText()
            product_name = product_hrefs.find(class_='goods-name').getText()
            obsh = product_brand + ' ' + product_name
            tag_name = 'extra_name_c'

            # if not self.check_exists(name, papka):
            #     continue

            if len(tag_list):
                for tag in tag_list:
                    if tag in obsh:
                        with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\{tag_name}.json", 'w',
                                  encoding='utf-8') as file:
                            json.dump(tag, file, indent=4, ensure_ascii=False)
                        break

            if self.prod_papka_yaratish_c(name, papka):
                parent_dir = f'{os.path.dirname(absolute_path)}\{name}'
                path = os.path.join(parent_dir, f'{papka}')
                os.mkdir(path)
                par_img = f'{os.path.dirname(absolute_path)}\{name}\{papka}'
                if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name}\{papka}\images'):
                    path_img = os.path.join(par_img, 'images')
                    os.mkdir(path_img)
            if self.check_exists(name, papka):
                continue
            else:
                response1 = self.get_html(f'https://www.wildberries.ru{product_href}')
                source1 = response1.text
                with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\product_detail.html", 'w',
                          encoding='utf-8') as file:
                    file.write(source1)

            with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\product_detail.html",
                      encoding='utf-8') as file:
                soup = file.read()
            source = BeautifulSoup(soup, 'lxml')

            try:
                brand_img_href = source.find(class_='same-part-kt__brand-logo').find('img').get('src')
                product_brand = source.find(class_='same-part-kt__header').find('span').get_text()
            except AttributeError as ex:
                continue
            if product_brand[-1:] == '.':
                product_brand_nam = product_brand.replace('.', '').replace('?', '')
            else:
                product_brand_nam = product_brand.replace('?', '')

            if '/' in product_brand_nam:
                product_brand_name1 = product_brand_nam.replace('/', '')
                product_brand_name = self.replace_drop(product_brand_name1)
            else:
                product_brand_name1 = product_brand_nam
                product_brand_name = self.replace_drop(product_brand_name1).replace('*','')

            if brand_img_href != None:
                brand1 = self.test_request(f'https:{brand_img_href}')
                brand = brand1.content
                b_name = product_brand_name
                with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\images\{b_name}.jpg",
                          'wb') as file:
                    file.write(brand)
                brand_name = 'brand'
                with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\{brand_name}.json", 'w',
                          encoding='utf-8') as file:
                    json.dump(product_brand_name, file, indent=4, ensure_ascii=False)

            if self.check_img_dir(name, papka, 'images'):
                prod_images = source.find(class_='same-part-kt').find(class_='swiper-wrapper').find_all('li')
                count_img = 1
                for prod_image in prod_images:
                    if 'slide--video' in prod_image['class']:
                        continue
                    else:
                        try:
                            image = prod_image.find('img').get('src')
                        except AttributeError as ex:
                            image = prod_image.find('source').get('srcset')
                        if 'c246x328' in image:
                            image=image.replace('c246x328','c516x688')
                        elif 'big' in image:
                            image = image.replace('big', 'c516x688')

                        req_img = self.test_request(f'https:{image}').content
                        # req_img = self.test_request(f'https:{image}').content
                        with open(
                                f"{os.path.dirname(absolute_path)}\{name}\{papka}\images\{papka}-{count_img}.jpg",'wb') as file:
                            file.write(req_img)
                        count_img += 1

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

            if not self.check_exists(name, papka):
                continue

            tag_name='extra_name_d'
            for tag in tag_list:
                if tag in obsh:
                    with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\{tag_name}.json", 'w',encoding='utf-8') as file:
                        json.dump(tag, file, indent=4, ensure_ascii=False)
                    break

            print(papka)
            continue
            if self.prod_papka_yaratish_c(name, papka):
                parent_dir = f'{os.path.dirname(absolute_path)}\{name}'
                path = os.path.join(parent_dir, f'{papka}')
                os.mkdir(path)
                par_img = f'{os.path.dirname(absolute_path)}\{name}\{papka}'
                if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name}\{papka}\images'):
                    path_img = os.path.join(par_img, 'images')
                    os.mkdir(path_img)
            if self.check_exists(name, papka):
                continue
            else:
                response1 = self.get_html(f'https://www.wildberries.ru{product_href}')
                source1 = response1.text
                with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\product_detail.html", 'w',
                          encoding='utf-8') as file:
                    file.write(source1)

            with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\product_detail.html",
                      encoding='utf-8') as file:
                soup = file.read()
            source = BeautifulSoup(soup, 'lxml')

            try:
                brand_img_href = source.find(class_='same-part-kt__brand-logo').find('img').get('src')
                product_brand = source.find(class_='same-part-kt__header').find('span').get_text()
            except AttributeError as ex:
                continue
            if product_brand[-1:] == '.':
                product_brand_nam = product_brand.replace('.', '').replace('?', '')
            else:
                product_brand_nam = product_brand.replace('?', '')

            if '/' in product_brand_nam:
                product_brand_name1 = product_brand_nam.replace('/', '')
                product_brand_name = self.replace_drop(product_brand_name1)
            else:
                product_brand_name1 = product_brand_nam
                product_brand_name = self.replace_drop(product_brand_name1).replace('*','')

            if brand_img_href != None:
                brand1 = self.test_request(f'https:{brand_img_href}')
                brand = brand1.content
                b_name = product_brand_name
                with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\images\{b_name}.jpg",
                          'wb') as file:
                    file.write(brand)
                brand_name = 'brand'
                with open(f"{os.path.dirname(absolute_path)}\{name}\{papka}\{brand_name}.json", 'w',
                          encoding='utf-8') as file:
                    json.dump(product_brand_name, file, indent=4, ensure_ascii=False)

            if self.check_img_dir(name, papka, 'images'):
                prod_images = source.find(class_='same-part-kt').find(class_='swiper-wrapper').find_all('li')
                count_img = 1
                for prod_image in prod_images:
                    if 'slide--video' in prod_image['class']:
                        continue
                    else:
                        try:
                            image = prod_image.find('img').get('src')
                        except AttributeError as ex:
                            image = prod_image.find('source').get('srcset')
                        if 'c246x328' in image:
                            image=image.replace('c246x328','c516x688')
                        elif 'big' in image:
                            image = image.replace('big', 'c516x688')

                        req_img = self.test_request(f'https:{image}').content
                        # req_img = self.test_request(f'https:{image}').content
                        with open(
                                f"{os.path.dirname(absolute_path)}\{name}\{papka}\images\{papka}-{count_img}.jpg",'wb') as file:
                            file.write(req_img)
                        count_img += 1


    def product_characters_cc(self, source, name1):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)

            try:
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\product_detail.html",
                          encoding='utf-8') as file:
                    soup = file.read()
            except FileNotFoundError as ex:
                continue

            source = BeautifulSoup(soup, 'lxml')
            try:
                caption = source.find(class_='product-params').find(class_='product-params__table').find('caption')
            except AttributeError as ex:
                continue

            if source.find(class_='same-part-kt__color')==None:
                continue
            if source.find(class_='same-part-kt__color').find('span') != None:
                colo = source.find(class_='same-part-kt__color').find('span').get_text()
                color = colo.replace(',', '-')
            else:
                color = ''
            caption_name = 'Общие характеристики'
            cap_dict = {}
            sub_cap_dict = {}
            model_dict = {}
            if caption != None:
                for a in caption.next_siblings:
                    if a.name == 'caption':
                        cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'
                        caption_name = a.get_text()
                        sub_cap_dict = {}
                    else:
                        if a.find('tr') != -1 and a.find('tr') != None:
                            sub_name = a.find('tr').find('th').find('span').find('span').get_text()
                            sub_val = a.find('tr').find('td').get_text()
                            sub_value = sub_val.split(';')
                            if sub_name == 'Модель':
                                name = 'model'
                                model_dict[f'{sub_name}'] = f'{sub_val}'
                                with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\{name}.json", 'w',
                                          encoding='utf-8') as file:
                                    json.dump(model_dict, file, indent=4, ensure_ascii=False)

                            sub_cap_dict[f'{sub_name}'] = f'{sub_value}'
                        else:
                            continue

                cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'

            else:
                for a in source.find(class_='product-params').find(class_='product-params__table').find_all('tbody'):
                    sub_name = a.find('tr').find('th').find('span').find('span').get_text()
                    sub_val = a.find('tr').find('td').get_text()
                    sub_value = sub_val.split(';')
                    if sub_name == 'Модель':
                        name = 'model'
                        model_dict[f'{sub_name}'] = f'{sub_val}'
                        with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\{name}.json", 'w',
                                  encoding='utf-8') as file:
                            json.dump(model_dict, file, indent=4, ensure_ascii=False)
                    sub_cap_dict[f'{sub_name}'] = f'{sub_value}'
                cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'

            descrip = {}
            for desc in source.find_all(class_='product-detail__details details'):
                description_title = desc.find('h2').get_text()
                description_text = desc.find(class_='details__content').find('p').get_text()
                descrip[f'{description_title}'] = f'{description_text}'
            descrip['color'] = f'{color}'

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\description.json", 'w',
                      encoding='utf-8') as file:
                json.dump(descrip, file, indent=4, ensure_ascii=False)

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\product_characters.json", 'w',
                      encoding='utf-8') as file:
                json.dump(cap_dict, file, indent=4, ensure_ascii=False)


    def product_characters_dd(self, source, name1):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            try:
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\product_detail.html",
                          encoding='utf-8') as file:
                    soup = file.read()
            except FileNotFoundError as ex:
                continue

            source = BeautifulSoup(soup, 'lxml')
            try:
                caption = source.find(class_='product-params').find(class_='product-params__table').find('caption')
            except AttributeError as ex:
                continue

            if source.find(class_='same-part-kt__color')==None:
                continue
            if source.find(class_='same-part-kt__color').find('span') != None:
                colo = source.find(class_='same-part-kt__color').find('span').get_text()
                color = colo.replace(',', '-')
            else:
                color = ''
            caption_name = 'Общие характеристики'
            cap_dict = {}
            sub_cap_dict = {}
            model_dict={}
            if caption != None:
                for a in caption.next_siblings:
                    if a.name == 'caption':
                        cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'
                        caption_name = a.get_text()
                        sub_cap_dict = {}
                    else:
                        if a.find('tr') != -1 and a.find('tr') != None:
                            sub_name = a.find('tr').find('th').find('span').find('span').get_text()
                            sub_val = a.find('tr').find('td').get_text()
                            sub_value = sub_val.split(';')
                            if sub_name == 'Модель':
                                name = 'model'
                                model_dict[f'{sub_name}'] = f'{sub_val}'
                                with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\{name}.json", 'w',
                                          encoding='utf-8') as file:
                                    json.dump(model_dict, file, indent=4, ensure_ascii=False)
                            sub_cap_dict[f'{sub_name}'] = f'{sub_value}'
                        else:
                            continue

                cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'

            else:
                for a in source.find(class_='product-params').find(class_='product-params__table').find_all('tbody'):
                    sub_name = a.find('tr').find('th').find('span').find('span').get_text()
                    sub_val = a.find('tr').find('td').get_text()
                    sub_value = sub_val.split(';')
                    if sub_name == 'Модель':
                        name = 'model'
                        model_dict[f'{sub_name}'] = f'{sub_val}'
                        with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\{name}.json", 'w',
                                  encoding='utf-8') as file:
                            json.dump(model_dict, file, indent=4, ensure_ascii=False)
                    sub_cap_dict[f'{sub_name}'] = f'{sub_value}'
                cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'

            descrip = {}
            for desc in source.find_all(class_='product-detail__details details'):
                description_title = desc.find('h2').get_text()
                description_text = desc.find(class_='details__content').find('p').get_text()
                descrip[f'{description_title}'] = f'{description_text}'
            descrip['color'] = f'{color}'

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\description.json", 'w',
                      encoding='utf-8') as file:
                json.dump(descrip, file, indent=4, ensure_ascii=False)

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\product_characters.json", 'w',
                      encoding='utf-8') as file:
                json.dump(cap_dict, file, indent=4, ensure_ascii=False)



    def product_attributes_c(self, source, category_name_id):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            try:
                json_data = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\product_characters.json")
            except FileNotFoundError as ex:
                continue
            print(papka)
            categor_idd=Categories.objects.filter(name=category_name_id)[:1].get().id
            for name, values in json_data.items():
                if not Branches.objects.filter(name=name).exists():
                    branch__tt = Branches(
                        name=name,
                        created_at='2021-07-01 17:44:48',
                        updated_at='2021-07-18 07:51:00',
                    )
                    branch__tt.save()
                    id = branch__tt.id
                    self.branch_translation(id, name=name)
                else:
                    id = Branches.objects.filter(name=name)[:1].get().id

                res = ast.literal_eval(values)
                for sub_name, sub_value in res.items():
                    if not Attributes.objects.filter(Q(branch_id=id) & Q(name=sub_name)).exists():
                        atributess = Attributes(
                            branch_id=id,
                            name=sub_name,
                            combination=0,
                            created_at='2021-05-20 20:14:08',
                            updated_at='2021-05-20 20:14:08',
                            deleted_at=None
                        )
                        atributess.save()
                        attr_id = atributess.id
                        self.attribute_translation(attr_id, name=sub_name)
                    else:
                        attr_id = Attributes.objects.filter(Q(branch_id=id) & Q(name=sub_name))[:1].get().id
                    self.put_category_and_attr(int(categor_idd), attr_id)

                for sub_name, sub_value in res.items():
                    print(sub_value)
                    x = ast.literal_eval(sub_value)
                    attribute_id = self.get_attributes(f'{sub_name}')
                    for char_val in range(0, len(x)):
                        cha_rem = self.remove_all_spaces(x[char_val].lower())
                        if ((cha_rem != '')and(cha_rem!='-')):
                            if not Characteristics.objects.filter(Q(name=cha_rem) & Q(attribute_id=attribute_id)).exists():
                                slug = self.get_slugify(f'{cha_rem}')
                                if int(self.slug_unique_for_chars(slug)) != 0:
                                    slug = slug + f'-{int(self.slug_unique_for_chars(slug))}'
                                pch = Characteristics(
                                    attribute_id=attribute_id,
                                    name=cha_rem,
                                    slug=slug,
                                    created_at='2021-05-29 00:55:49',
                                    updated_at='2021-05-20 21:05:09',
                                    deleted_at=None,
                                )
                                pch.save()
                                char_id = pch.id
                                self.char_translation(char_id, name=cha_rem)


            brand_n = 'brand'
            a1 = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\{brand_n}.json")
            a=a1#json.loads(a1)
            if a[-1:] == '.':
                product_brand_nam = a.replace('.', '')
            else:
                product_brand_nam = a

            if '/' in product_brand_nam:
                b_name = product_brand_nam.replace('/', '')
            else:
                b_name = product_brand_nam

            file_size = os.path.getsize(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\images\{b_name}.jpg")
            if not Uploads.objects.filter(file_original_name=b_name).exists():
                file_name = self.hash_and_move(b_name,f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\images\{b_name}.jpg")
                ##################### Uploadsssssssss#################
                name_b='brand'
                brand_id = self.uploads(b_name, file_name, file_size,name_b)

            slug = self.get_slugify(f'{b_name}')
            if int(self.slug_unique_for_brand(slug)) != 0:
                slug = slug + f'-{int(self.slug_unique_for_brand(slug))}'
            if not Brands.objects.filter(name=b_name).exists():
                brad_id = Uploads.objects.filter(file_original_name=f'{b_name}')[:1].get().id
                pb = Brands(
                    name=b_name,
                    logo=brad_id,
                    top=0,
                    slug=slug,
                    meta_title=f'{b_name} в онлайн гипермаркете TINFIS',
                    meta_description=f'Огромный выбор продукции бренда "{b_name}" в нашем онлайн гипермаркете.  100% гарантия качества от лучших магазинов!',
                    created_at='2021-05-21 02:19:37',
                    updated_at='2021-05-21 02:19:37'
                )
                pb.save()
                brand_id = pb.id
                self.brand_translation(brand_id, name=b_name)
            cater_id =categor_idd
            brand_id = Brands.objects.filter(name=f"{b_name}")[:1].get().id
            if not BrandCategory.objects.filter(Q(brand_id=brand_id) & Q(category_id=cater_id)).exists():
                BrandCategory(
                    brand_id=brand_id,
                    category_id=cater_id
                ).save()
            color = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\description.json")['color']
            if not Colors.objects.filter(name=color).exists():
                if color != '':
                    pc = Colors(
                        name=color,
                        code='#CD5C5C',
                        created_at='2018-11-04 19:12:26',
                        updated_at='2018-11-04 19:12:26'
                    )
                    pc.save()
                    color_id = pc.id
                    self.color_translation(color_id, name=color)



    def product_attributes_d(self, source, category_name_id):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            try:
                json_data = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\product_characters.json")
            except FileNotFoundError as ex:
                continue
            print(papka)

            for name, values in json_data.items():
                if not Branches.objects.filter(name=name).exists():
                    branch__tt = Branches(
                        name=name,
                        created_at='2021-07-01 17:44:48',
                        updated_at='2021-07-18 07:51:00',
                    )
                    branch__tt.save()
                    id = branch__tt.id
                    self.branch_translation(id, name=name)
                else:
                    id = Branches.objects.filter(name=name)[:1].get().id
                cate_iddd = Categories.objects.filter(name=category_name_id)[:1].get().id
                res = ast.literal_eval(values)
                for sub_name, sub_value in res.items():
                    if not Attributes.objects.filter(Q(branch_id=id) & Q(name=sub_name)).exists():
                        atributess = Attributes(
                            branch_id=id,
                            name=sub_name,
                            combination=0,
                            created_at='2021-05-20 20:14:08',
                            updated_at='2021-05-20 20:14:08',
                            deleted_at=None
                        )
                        atributess.save()
                        attr_id = atributess.id
                        self.attribute_translation(attr_id, name=sub_name)
                    else:
                        attr_id = Attributes.objects.filter(Q(branch_id=id) & Q(name=sub_name))[:1].get().id

                    self.put_category_and_attr(cate_iddd, attr_id)

                for sub_name, sub_value in res.items():
                    print(sub_value)
                    x = ast.literal_eval(sub_value)
                    attribute_id = self.get_attributes(f'{sub_name}')
                    for char_val in range(0, len(x)):
                        cha_rem = self.remove_all_spaces(x[char_val].lower())
                        if ((cha_rem != '')and(cha_rem!='-')):
                            if not Characteristics.objects.filter(Q(name=cha_rem) & Q(attribute_id=attribute_id)).exists():
                                slug = self.get_slugify(f'{cha_rem}')
                                if int(self.slug_unique_for_chars(slug)) != 0:
                                    slug = slug + f'-{int(self.slug_unique_for_chars(slug))}'
                                pch = Characteristics(
                                    attribute_id=attribute_id,
                                    name=cha_rem,
                                    slug=slug,
                                    created_at='2021-05-29 00:55:49',
                                    updated_at='2021-05-20 21:05:09',
                                    deleted_at=None,
                                )
                                pch.save()
                                char_id = pch.id
                                self.char_translation(char_id, name=cha_rem)


            brand_n = 'brand'
            a1 = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\{brand_n}.json")
            a=json.loads(a1)
            if a[-1:] == '.':
                product_brand_nam = a.replace('.', '')
            else:
                product_brand_nam = a

            if '/' in product_brand_nam:
                b_name = product_brand_nam.replace('/', '')
            else:
                b_name = product_brand_nam

            file_size = os.path.getsize(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\images\{b_name}.jpg")
            if not Uploads.objects.filter(file_original_name=b_name).exists():
                file_name = self.hash_and_move(b_name,f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\images\{b_name}.jpg")
                ##################### Uploadsssssssss#################
                name_b='brand'
                brand_id = self.uploads(b_name, file_name, file_size,name_b)

            slug = self.get_slugify(f'{b_name}')
            if int(self.slug_unique_for_brand(slug)) != 0:
                slug = slug + f'-{int(self.slug_unique_for_brand(slug))}'
            if not Brands.objects.filter(name=b_name).exists():
                brad_id = Uploads.objects.filter(file_original_name=f'{b_name}')[:1].get().id
                pb = Brands(
                    name=b_name,
                    logo=brad_id,
                    top=0,
                    slug=slug,
                    meta_title=f'{b_name} в онлайн гипермаркете TINFIS',
                    meta_description=f'Огромный выбор продукции бренда "{b_name}" в нашем онлайн гипермаркете.  100% гарантия качества от лучших магазинов!',
                    created_at='2021-05-21 02:19:37',
                    updated_at='2021-05-21 02:19:37'
                )
                pb.save()
                brand_id = pb.id
                self.brand_translation(brand_id, name=b_name)
            cater_id =cate_iddd
            brand_id = Brands.objects.filter(name=f"{b_name}")[:1].get().id
            if not BrandCategory.objects.filter(Q(brand_id=brand_id) & Q(category_id=cater_id)).exists():
                BrandCategory(
                    brand_id=brand_id,
                    category_id=cater_id
                ).save()
            color = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\description.json")['color']
            if not Colors.objects.filter(name=color).exists():
                if color != '':
                    pc = Colors(
                        name=color,
                        code='#CD5C5C',
                        created_at='2018-11-04 19:12:26',
                        updated_at='2018-11-04 19:12:26'
                    )
                    pc.save()
                    color_id = pc.id
                    self.color_translation(color_id, name=color)



    def prod_papka_yaratish_c(self, cate_name, nomi):
        absolute_path = os.path.abspath(__file__)
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{cate_name}\{nomi}'):
            return True
        else:
            return False

    def replace_drop(self, brand):
        x = ''
        for a in brand:
            if a == '/':
                x += ' '
                continue
            else:
                if a == "\\":
                    x += ' '
                    continue
                else:
                    x += a
        return x

    def put_category_and_attr(self, cate_name, atr_id):
        if not AttributeCategory.objects.filter(Q(attribute_id=f'{atr_id}') & Q(category_id=cate_name)).exists():
            p = AttributeCategory(
                attribute_id=atr_id,
                category_id=cate_name
            ).save()

    def uploads(self, name, file_name, file_size, t_name):
        n = 'all'
        p = Uploads(
            file_original_name=name,
            file_name=f'uploads\{n}\{file_name}.jpg',
            user_id=9,
            file_size=file_size,
            extension='jpg',
            model_type=t_name,
            type='image',
            created_at='2021-05-29 00:55:49',
            updated_at='2021-07-08 13:47:28',
            deleted_at=None
        ).save()
        return Uploads.objects.filter(file_original_name=name)[:1].get().id

    def read_json(self,path):
        return json.loads(self.read_file(path))

    def get_category_id(self,name):
        return Categories.objects.filter(name=name)[:1].get().id

    def slug_unique_for_product(self, slug):
        if Products.objects.filter(slug__startswith=slug).exists():
            a = Products.objects.filter(slug__startswith=slug).count()
            print(Products.objects.filter(slug__startswith=slug)[:1].get().slug)
            return a
        else:
            return 0


    def slug_unique_for_var(self,slug):
        if Variations.objects.filter(slug__startswith=slug).exists():
            a=Variations.objects.filter(slug__startswith=slug).count()
            print(Variations.objects.filter(slug__startswith=slug)[:1].get().slug)
            return a
        else:
            return 0


    def slug_unique_for_chars(self,slug):
        if Characteristics.objects.filter(slug__startswith=slug).exists():
            a=Characteristics.objects.filter(slug__startswith=slug).count()
            return a
        else:
            return 0

    def slug_unique_for_elem(self,slug):
        if Elements.objects.filter(slug__startswith=slug).exists():
            a=Elements.objects.filter(slug__startswith=slug).count()
            return a
        else:
            return 0

    def slug_unique_for_brand(self,slug):
        if Brands.objects.filter(slug__startswith=slug).exists():
            a=Brands.objects.filter(slug__startswith=slug).count()
            return a
        else:
            return 0

    def join_dicts(self,d1, d2):
        k1 = []
        k2 = []
        for k in d1.keys():
            k1.append(k)
        for k in d2.keys():
            k2.append(k)
        atributes_outer=[]
        for k in k1:
            if k not in k2:
                list_d1 = d1[f'{k}']
                d2[f'{k}'] = list_d1
                atributes_outer.append(k)
            else:
                a = d1[f'{k}']
                b = d2[f'{k}']
                resultList = list(set(a) | set(b))
                d2[f'{k}'] = resultList
        return {'umumiy':d2,'atr_combinations':atributes_outer}


    def put_elements_c(self, source, category_name,extra_name_c):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)


        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            if not os.path.isdir(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}"):
                continue
            print(papka)

            name='brand'
            if not (os.path.exists(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json") and os.path.getsize(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json") != 0):
                continue
            br1=self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json")
            bran=br1#json.loads(br1)

            name_ext='extra_name_c'
            tag_id=''
            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name_ext}.json"):
                name_t=self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name_ext}.json")
                tag_id=Categories.objects.filter(name=name_t)[:1].get().id

            if extra_name_c!='':
                p=f'{extra_name_c} {bran}'
            else:
                p = f'{category_name} {bran}'

            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\model.json"):
                model_name= self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\model.json")
            else:
                continue

            if bran[-1:] == '.':
                brand = bran.replace('.', '')
            else:
                brand =bran
            if '/' in brand:
                brand=brand.replace('/','')

            cate_id = ''
            cate_id = Categories.objects.filter(name=f'{category_name}')[:1].get().id
            brand_id = Brands.objects.filter(name=brand)[:1].get().id
            if not BrandCategory.objects.filter(Q(brand_id=brand_id) & Q(category_id=cate_id)).exists():
                BrandCategory(
                    brand_id=brand_id,
                    category_id=cate_id
                ).save()
            pro_name=p.replace('.','')
            diagonal=''
            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\diagonal.json"):
                diagonal = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\diagonal.json")

            model_a=self.cut_model(model_name['Модель'],bran,diagonal)
            # print(model_a)
            mal=self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\description.json")
            color = mal['color']
            memory=''
            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\memory.json"):
                memory = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\memory.json")['Объем встроенной памяти (Гб)']


            ann=f'{pro_name} {model_a.strip()}'
            if memory !='':
                var_name=ann+', '+memory+', '+color
            else:
                var_name = ann + ', ' + color

            description = mal['Описание']
            json_data = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\product_characters.json")
            attr_diction_umumiy = {}
            ves = 0
            aaa = ''
            branch_list=[]
            for name, values in json_data.items():
                branch_1_dict = {}
                branch1_id=Branches.objects.filter(name=name)[:1].get().id
                branch_1_dict['id']=branch1_id
                branch_1_dict['title']=f'{name}'
                res = ast.literal_eval(values)
                atrd_list=[]
                for sub_name, sub_value in res.items():
                    attribute_dict = {}
                    charak_list = []
                    if sub_name == 'Вес товара с упаковкой (г)':
                        ves = int(float(sub_value.replace('[', '').replace(']', '').replace(' ', '').replace('г', '').replace("'","")))
                    char_dict = ast.literal_eval(sub_value)
                    attri_id = Attributes.objects.filter(Q(name=sub_name) & Q(branch_id=branch1_id))[:1].get().id
                    attribute_dict['id'] = attri_id
                    attribute_dict['attribute'] = f'{sub_name}'
                    char_l=[]
                    for char in char_dict:
                        char_name = self.remove_all_spaces(char.lower())
                        if ((char_name!='')and(char_name!='-')):
                            if not Characteristics.objects.filter(Q(attribute_id=attri_id) & Q(name=char_name)).exists():
                                slug = self.get_slugify(f'{char_name}')
                                if int(self.slug_unique_for_chars(slug)) != 0:
                                    slug = slug + f'-{int(self.slug_unique_for_chars(slug))}'
                                Characteristics(
                                    attribute_id=attri_id,
                                    name=char_name,
                                    slug=slug,
                                    created_at='2021-05-29 00:55:49',
                                    updated_at='2021-05-29 00:55:49',
                                    deleted_at=None
                                ).save()
                            char_id = Characteristics.objects.filter(Q(attribute_id=attri_id) & Q(name=char_name))[:1].get().id
                            charak_list.append(f'{char_id}')
                            c_a={}
                            ggg=str(char_id)
                            c_a['id']=int(ggg.replace('(),',''))
                            c_a['name']=f'{char_name}'
                            char_l.append(c_a)
                    attribute_dict['values']=char_l
                    atrd_list.append(attribute_dict)
                    attr_diction_umumiy[f'{attri_id}'] = charak_list
                branch_1_dict['options']=atrd_list
                branch_list.append(branch_1_dict)
            oxirgi={}
            oxirgi['en']=branch_list
            oxirgi['ru'] = branch_list
            oxirgi['uz'] = branch_list


            app_json = json.dumps(attr_diction_umumiy)
            category_iddd=Categories.objects.filter(name=category_name)[:1].get().id

            if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-1.jpg'):
                continue
            if not Elements.objects.filter(Q(name=f"{ann}") & Q(category_id=category_iddd) & Q(brand_id=brand_id)).exists():
                if color!='':
                    var_a = ann+', '+color
                else:
                    var_a = ann
                co=[]
                if color!='':
                    color_id=Colors.objects.filter(name=color)[:1].get().id
                    co.append(f'{color_id}')
                    color_json = json.dumps(co)
                else:
                    color_json=None
                    color_id=None

                photo_thum_list=''
                photo_list = ''
                for i in range(1,50):
                    if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg'):
                        break
                    else:
                        file_name=self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')
                        file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')

                        if not Uploads.objects.filter(file_original_name=f'{papka}-{i}').exists():
                            file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')
                            b_name1 = 'element'
                            photos_id = self.uploads(f'{papka}-{i}', file_name, file_size, b_name1)
                        else:
                            photos_id = Uploads.objects.filter(file_original_name=f'{papka}-{i}')[:1].get().id

                        if i == 1:
                            photo_thum_list+=f'{photos_id}'
                        else:
                            if i==2:
                                photo_list+=f'{photos_id}'
                            else:
                                photo_list+=f',{photos_id}'
                photo_id_json=photo_list
                photo_thum_json = photo_thum_list
                elem_slug=self.get_slugify(f'{ann}')
                if int(self.slug_unique_for_elem(elem_slug))!=0:
                    elem_slug = elem_slug + f'-{int(self.slug_unique_for_elem(elem_slug))}'

                element_qosh = Elements(
                    name=ann,
                    added_by='admin',
                    user_id=9,
                    category_id=cate_id,
                    parent_id=0,
                    brand_id=brand_id,
                    photos=photo_thum_json,
                    thumbnail_img=photo_thum_json,
                    video_provider='youtube',
                    video_link='',
                    tags=tag_id,
                    description=description,
                    short_description=json.dumps(oxirgi,ensure_ascii=False),
                    characteristics=app_json,
                    variations='[]',
                    variation_attributes='[]',
                    variation_colors=color_json,
                    todays_deal=1,
                    published=1,
                    featured=1,
                    unit='pcs',
                    weight=float(ves)/1000,
                    num_of_sale=0,
                    meta_title=pro_name,
                    meta_description=description,
                    meta_img='',
                    pdf='',
                    slug=elem_slug,
                    earn_point=random.randint(20,100)*100,
                    rating=random.randint(0,5),
                    barcode=papka,
                    digital=1,
                    file_name='',
                    file_path='',
                    created_at='2021-06-28 08:43:07',
                    updated_at='2021-06-28 08:43:07',
                    on_moderation=0,
                    is_accepted=1,
                    refundable=1,
                )
                element_qosh.save()
                self.elem_translation(element_qosh.id,ann,description)
                variation = Variations(
                    name=var_a,
                    lowest_price_id=0,
                    slug=elem_slug,
                    partnum=papka,
                    element_id=element_qosh.id,
                    prices=random.randint(1,10)*100,
                    variant='',
                    description=description,
                    short_description=json.dumps(oxirgi,ensure_ascii=False),
                    created_at='2021-08-01 16:32:32',
                    updated_at='2021-08-01 16:32:32',
                    user_id=9,
                    num_of_sale=0,
                    qty=0,
                    rating=random.randint(0,5),
                    thumbnail_img=photo_thum_json,
                    photos=photo_id_json,
                    color_id=color_id,
                    characteristics=None,
                    deleted_at=None,
                )
                variation.save()
                self.var_translation(variation.id,var_a)
                sel = [3, 52, 69]
                pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                for i in range(0, 3):
                    var_a1 = var_a + pro_names[i]
                    pro_slug = self.get_slugify(f'{var_a1}')
                    if int(self.slug_unique_for_product(pro_slug)) != 0:
                        pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                    p=Products(
                        name=var_a1,
                        slug=pro_slug,
                        user_id=sel[i],
                        added_by='seller',
                        currency_id=1,
                        price=random.randint(1,10)*100,
                        discount=random.randint(0,10),
                        discount_type='percent',
                        discount_start_date=None,
                        discount_end_date=None,
                        variation_id=variation.id,
                        todays_deal=1,
                        num_of_sale=15,
                        delivery_type='tarif',
                        qty=10,
                        est_shipping_days=None,
                        low_stock_quantity=None,
                        published=1,
                        approved=1,
                        stock_visibility_state='quantity',
                        cash_on_delivery=1,
                        tax=random.randint(1,10),
                        tax_type='percent',
                        created_at='2021-09-13 20:22:42',
                        updated_at='2021-09-13 20:22:42',
                        featured=1,
                        seller_featured=0,
                        refundable=1,
                        on_moderation=0,
                        is_accepted=1,
                        digital=0,
                        rating=random.randint(0,5),
                        barcode=papka,
                        earn_point=random.randint(20,100)*100,
                        element_id=element_qosh.id,
                        sku=None,
                        deleted_at=None,
                        is_quantity_multiplied=0
                    ).save()
            else:
                bran_rr_id=Branches.objects.filter(name="Память")[:1].get().id
                Attributes.objects.filter(Q(name="Объем встроенной памяти (Гб)") & Q(branch_id=bran_rr_id)).update(combination=1)
                elem_id = Elements.objects.filter(Q(name=ann) & Q(category_id=category_iddd) & Q(brand_id=brand_id))[:1].get().id
                variat_json = Elements.objects.filter(id=elem_id)[:1].get().variations
                var_json_colors=Elements.objects.filter(id=elem_id)[:1].get().variation_colors
                element_characters=json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                new_rel=self.join_dicts(attr_diction_umumiy,element_characters)
                new_char=new_rel['umumiy']
                if len(new_rel['atr_combinations']):
                    for a in new_rel['atr_combinations']:
                        Attributes.objects.filter(id=a).update(combination=1)

                Elements.objects.filter(id=elem_id).update(characteristics=json.dumps(new_char))
                if var_json_colors!=None:
                    variation_colors=json.loads(var_json_colors)
                else:
                    variation_colors=None
                if color !='':
                    color_id = Colors.objects.filter(name=color)[:1].get().id
                else:
                    color_id=None

                rangi = False
                if color_id !=None:
                    if variation_colors==None:
                        variation_colors=list()
                        variation_colors.append(f'{color_id}')
                    elif f'{color_id}' not in variation_colors:
                        variation_colors.append(f'{color_id}')
                        rangi = True
                    variat_json_color1=json.dumps(variation_colors)
                    variat_json_color=self.remove_space(variat_json_color1)
                    Elements.objects.filter(id=elem_id).update(variation_colors=variat_json_color)
                if memory !="":
                    attri_id = Attributes.objects.filter(Q(name="Объем встроенной памяти (Гб)") & Q(branch_id=bran_rr_id))[:1].get().id
                    memory_id = Characteristics.objects.filter(Q(name=f"{self.remove_all_spaces(memory.lower())}")&Q(attribute_id=attri_id))[:1].get().id
                else:
                    memory_id=None
                if Variations.objects.filter(Q(element_id=elem_id) &Q(color_id=color_id)&Q(characteristics=memory_id)).exists():
                    continue
                if variat_json =='[]':
                    m_dict = {}
                    m_list = []
                    m1 = []
                    if memory != "":
                        m_list.append(f'{memory_id}')
                        m_dict[f'{attri_id}'] = m_list
                        print(f'{variat_json}---keyin----{m_list}')
                        m1.append(f'{attri_id}')
                        a2 = json.dumps(m_dict)
                        m2 = json.dumps(m1)
                        print(f'a2={a2} -----m2={m2} ')
                        elem_char_m=json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                        aa1=list(elem_char_m[f'{attri_id}'])
                        if f'{memory_id}' not in aa1:
                            aa1.append(f'{memory_id}')
                        elem_char_m[f'{attri_id}']=aa1
                        aa2=json.dumps(elem_char_m)
                        Elements.objects.filter(id=elem_id).update(characteristics=aa2,variations=a2, variation_attributes=m2)
                else:
                    if memory !="":
                        a1=json.loads(variat_json)
                        if f'{attri_id}' in a1.keys():
                            a2=list(a1[f'{attri_id}'])
                            if f'{memory_id}' not in a2:
                                a2.append(f'{memory_id}')
                                a1[f'{attri_id}']=a2
                                elem_char_m = json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                                aa1 = list(elem_char_m[f'{attri_id}'])
                                if f'{memory_id}' not in aa1:
                                    aa1.append(f'{memory_id}')
                                elem_char_m[f'{attri_id}'] = aa1
                                aa2 = json.dumps(elem_char_m)
                                Elements.objects.filter(id=elem_id).update(characteristics=aa2,variations=json.dumps(a1))
                        elif f'{attri_id}' not in a1.keys():
                            d=[]
                            for aak in a1.keys():
                                d.append(f'{aak}')
                            elem_char_m = json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                            aa1 = list(elem_char_m[f'{attri_id}'])
                            if f'{memory_id}' not in aa1:
                                aa1.append(f'{memory_id}')
                            elem_char_m[f'{attri_id}'] = aa1
                            aa2 = json.dumps(elem_char_m)
                            a1[f'{attri_id}']=list(f'{memory_id}')
                            Elements.objects.filter(id=elem_id).update(characteristics=aa2,variations=json.dumps(a1),variation_attributes=json.dumps(d))

                phot_list=''
                photo_thum=''

                if not Variations.objects.filter(name=var_name).exists():
                    for i in range(1, 50):
                        if os.path.isfile(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg'):
                            file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')

                            if not Uploads.objects.filter(file_original_name=f'{papka}-{i}').exists():
                                file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')
                                b_name1 = 'variation'
                                photos_id = self.uploads(f'{papka}-{i}', file_name, file_size, b_name1)
                            else:
                                photos_id = Uploads.objects.filter(file_original_name=f'{papka}-{i}')[:1].get().id

                            if i == 1:
                                photo_thum+=f'{photos_id}'
                                ranglar = ''
                                if rangi:
                                    ranglar = Elements.objects.filter(id=elem_id)[:1].get().photos
                                    a_rrr = ranglar.split(',')
                                    a_rrr.append(f'{photos_id}')
                                    r_hamma = f'{a_rrr[0]}'
                                    for rr in a_rrr[1:]:
                                        r_hamma += f',{rr}'
                                    Elements.objects.filter(id=elem_id).update(photos=r_hamma)
                            else:
                                if i==2:
                                    phot_list+=f'{photos_id}'
                                else:
                                    phot_list+=f',{photos_id}'
                        else:
                            break
                    phot_list_json=phot_list
                    photo_thum_json=photo_thum
                    var_slug=self.get_slugify(f'{var_name}')
                    if int(self.slug_unique_for_var(var_slug))!=0:
                        var_slug=var_slug+f'-{int(self.slug_unique_for_var(var_slug))}'

                    if memory =="":
                        variation = Variations(
                            name=var_name,
                            lowest_price_id=0,
                            slug=var_slug,
                            partnum=papka,
                            element_id=elem_id,
                            prices=random.randint(1,10)*100,
                            variant='',
                            description=description,
                            short_description=json.dumps(oxirgi,ensure_ascii=False),
                            created_at='2021-08-01 16:32:32',
                            updated_at='2021-08-01 16:32:32',
                            user_id=9,
                            num_of_sale=random.randint(1,100),
                            qty=0,
                            rating=random.randint(0,5),
                            thumbnail_img=photo_thum_json,
                            photos=phot_list_json,
                            color_id=color_id,
                            characteristics=None,
                            deleted_at=None,
                        )
                        variation.save()
                        self.var_translation(variation.id, var_name)
                        sel = [3, 52, 69]
                        pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                        for i in range(0, 3):
                            var_a1 = var_name + pro_names[i]
                            pro_slug = self.get_slugify(f'{var_name}')
                            if int(self.slug_unique_for_product(pro_slug)) != 0:
                                pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                            p = Products(
                                name=var_a1,
                                slug=pro_slug,
                                user_id=sel[i],
                                added_by='seller',
                                currency_id=1,
                                price=random.randint(1, 10) * 100,
                                discount=random.randint(0, 10),
                                discount_type='percent',
                                discount_start_date=None,
                                discount_end_date=None,
                                variation_id=variation.id,
                                todays_deal=1,
                                num_of_sale=15,
                                delivery_type='tarif',
                                qty=10,
                                est_shipping_days=None,
                                low_stock_quantity=None,
                                published=1,
                                approved=1,
                                stock_visibility_state='quantity',
                                cash_on_delivery=1,
                                tax=random.randint(1, 10),
                                tax_type='percent',
                                created_at='2021-09-13 20:22:42',
                                updated_at='2021-09-13 20:22:42',
                                featured=1,
                                seller_featured=0,
                                refundable=1,
                                on_moderation=0,
                                is_accepted=1,
                                digital=0,
                                rating=random.randint(0, 5),
                                barcode=papka,
                                earn_point=random.randint(20, 100) * 100,
                                element_id=elem_id,
                                sku=None,
                                deleted_at=None,
                                is_quantity_multiplied=0
                            ).save()


                    else:
                        memory_id1 = Characteristics.objects.filter(name=f"{self.remove_all_spaces(memory.lower())}")[:1].get().id
                        print(f'memory_id={memory_id1}')
                        variation = Variations(
                            name=var_name,
                            lowest_price_id=0,
                            slug=var_slug,
                            partnum=papka,
                            element_id=elem_id,
                            prices=random.randint(1,10)*100,
                            variant='',
                            description=description,
                            short_description=json.dumps(oxirgi,ensure_ascii=False),
                            created_at='2021-08-01 16:32:32',
                            updated_at='2021-08-01 16:32:32',
                            user_id=9,
                            num_of_sale=random.randint(1,100),
                            qty=0,
                            rating=random.randint(0,5),
                            thumbnail_img=photo_thum_json,
                            photos=phot_list_json,
                            color_id=color_id,
                            characteristics=memory_id1,
                            deleted_at=None,
                        )
                        variation.save()
                        self.var_translation(variation.id, var_name)
                        sel = [3, 52, 69]
                        pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                        for i in range(0, 3):
                            var_a1 = var_name + pro_names[i]
                            pro_slug = self.get_slugify(f'{var_a1}')
                            if int(self.slug_unique_for_product(pro_slug)) != 0:
                                pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                            p = Products(
                                name=var_a1,
                                slug=pro_slug,
                                user_id=sel[i],
                                added_by='seller',
                                currency_id=1,
                                price=random.randint(1, 10) * 100,
                                discount=random.randint(0, 10),
                                discount_type='percent',
                                discount_start_date=None,
                                discount_end_date=None,
                                variation_id=variation.id,
                                todays_deal=1,
                                num_of_sale=15,
                                delivery_type='tarif',
                                qty=10,
                                est_shipping_days=None,
                                low_stock_quantity=None,
                                published=1,
                                approved=1,
                                stock_visibility_state='quantity',
                                cash_on_delivery=1,
                                tax=random.randint(1, 10),
                                tax_type='percent',
                                created_at='2021-09-13 20:22:42',
                                updated_at='2021-09-13 20:22:42',
                                featured=1,
                                seller_featured=0,
                                refundable=1,
                                on_moderation=0,
                                is_accepted=1,
                                digital=0,
                                rating=random.randint(0, 5),
                                barcode=papka,
                                earn_point=random.randint(20, 100) * 100,
                                element_id=elem_id,
                                sku=None,
                                deleted_at=None,
                                is_quantity_multiplied=0
                            ).save()

    def put_elements_d(self, source, category_name):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)

        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{category_name}\images'):
            parent_dir = f'{os.path.dirname(absolute_path)}\{category_name}'
            path = os.path.join(parent_dir, f'images')
            os.mkdir(path)

        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            if not os.path.isdir(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}"):
                continue
            print(papka)

            name='brand'
            if not (os.path.exists(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json") and os.path.getsize(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json") != 0):
                continue
            br1=self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name}.json")
            bran=json.loads(br1)

            name_d='extra_name_d'
            extra_name_d=self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{name_d}.json")

            p=f'{extra_name_d} {bran}'

            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\model.json"):
                model_name= self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\model.json")
            else:
                continue
            if bran[-1:] == '.':
                brand = bran.replace('.', '')
            else:
                brand =bran
            if '/' in brand:
                brand=brand.replace('/','')

            cate_id = ''
            cate_id = Categories.objects.filter(name=f'{category_name}')[:1].get().id
            brand_id = Brands.objects.filter(name=brand)[:1].get().id
            if not BrandCategory.objects.filter(Q(brand_id=brand_id) & Q(category_id=cate_id)).exists():
                BrandCategory(
                    brand_id=brand_id,
                    category_id=cate_id
                ).save()
            pro_name=p.replace('.','')
            diagonal=''

            tag_id=Categories.objects.filter(name=extra_name_d)[:1].get().id

            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\diagonal.json"):
                diagonal = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\diagonal.json")

            model_a=self.cut_model(model_name['Модель'],bran,diagonal)
            # print(model_a)
            mal=self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\description.json")
            color = mal['color']
            memory=''
            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\memory.json"):
                memory = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\memory.json")['Объем встроенной памяти (Гб)']


            ann=f'{pro_name} {model_a.strip()}'
            if memory !='':
                var_name=ann+', '+memory+', '+color
            else:
                var_name = ann + ', ' + color

            description = mal['Описание']
            ######Character###########
            json_data = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\product_characters.json")
            attr_diction_umumiy = {}
            ves = 0
            aaa = ''
            branch_list=[]
            for name, values in json_data.items():
                branch_1_dict = {}
                branch1_id=Branches.objects.filter(name=name)[:1].get().id
                branch_1_dict['id']=branch1_id
                branch_1_dict['title']=f'{name}'
                res = ast.literal_eval(values)
                atrd_list=[]
                for sub_name, sub_value in res.items():
                    attribute_dict = {}
                    charak_list = []
                    if sub_name == 'Вес товара с упаковкой (г)':
                        ves = int(float(sub_value.replace('[', '').replace(']', '').replace(' ', '').replace('г', '').replace("'","")))
                    char_dict = ast.literal_eval(sub_value)
                    attri_id = Attributes.objects.filter(Q(name=sub_name) & Q(branch_id=branch1_id))[:1].get().id
                    attribute_dict['id'] = attri_id
                    attribute_dict['attribute'] = f'{sub_name}'
                    char_l=[]
                    for char in char_dict:
                        char_name = self.remove_all_spaces(char.lower())
                        if ((char_name!='')and(char_name!='-')):
                            if not Characteristics.objects.filter(Q(attribute_id=attri_id) & Q(name=char_name)).exists():
                                slug = self.get_slugify(f'{char_name}')
                                if int(self.slug_unique_for_chars(slug)) != 0:
                                    slug = slug + f'-{int(self.slug_unique_for_chars(slug))}'
                                Characteristics(
                                    attribute_id=attri_id,
                                    name=char_name,
                                    slug=slug,
                                    created_at='2021-05-29 00:55:49',
                                    updated_at='2021-05-29 00:55:49',
                                    deleted_at=None
                                ).save()
                            char_id = Characteristics.objects.filter(Q(attribute_id=attri_id) & Q(name=char_name))[:1].get().id
                            charak_list.append(f'{char_id}')
                            c_a={}
                            ggg=str(char_id)
                            c_a['id']=int(ggg.replace('(),',''))
                            c_a['name']=f'{char_name}'
                            char_l.append(c_a)
                    attribute_dict['values']=char_l
                    atrd_list.append(attribute_dict)
                    attr_diction_umumiy[f'{attri_id}'] = charak_list
                branch_1_dict['options']=atrd_list
                branch_list.append(branch_1_dict)
            oxirgi={}
            oxirgi['en']=branch_list
            oxirgi['ru'] = branch_list
            oxirgi['uz'] = branch_list


            app_json = json.dumps(attr_diction_umumiy)
            category_iddd=Categories.objects.filter(name=category_name)[:1].get().id

            if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-1.jpg'):
                continue

            if not Elements.objects.filter(Q(name=f"{ann}") & Q(category_id=category_iddd) & Q(brand_id=brand_id)).exists():
                if color!='':
                    var_a = ann+', '+color
                else:
                    var_a = ann
                co=[]
                if color!='':
                    color_id=Colors.objects.filter(name=color)[:1].get().id
                    co.append(f'{color_id}')
                    color_json = json.dumps(co)
                else:
                    color_json=None
                    color_id=None

                photo_thum_list=''
                photo_list = ''
                for i in range(1,50):
                    if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg'):
                        break
                    else:
                        file_name=self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')
                        file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')

                        if not Uploads.objects.filter(file_original_name=f'{papka}-{i}').exists():
                            file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')
                            b_name1 = 'element'
                            photos_id = self.uploads(f'{papka}-{i}', file_name, file_size, b_name1)
                        else:
                            photos_id = Uploads.objects.filter(file_original_name=f'{papka}-{i}')[:1].get().id

                        if i == 1:
                            photo_thum_list+=f'{photos_id}'
                        else:
                            if i==2:
                                photo_list+=f'{photos_id}'
                            else:
                                photo_list+=f',{photos_id}'
                photo_id_json=photo_list
                photo_thum_json = photo_thum_list
                elem_slug=self.get_slugify(f'{ann}')
                if int(self.slug_unique_for_elem(elem_slug))!=0:
                    elem_slug = elem_slug + f'-{int(self.slug_unique_for_elem(elem_slug))}'

                element_qosh = Elements(
                    name=ann,
                    added_by='admin',
                    user_id=9,
                    category_id=cate_id,
                    parent_id=0,
                    brand_id=brand_id,
                    photos=photo_thum_json,
                    thumbnail_img=photo_thum_json,
                    video_provider='youtube',
                    video_link='',
                    tags=f'{tag_id}',
                    description=description,
                    short_description=json.dumps(oxirgi,ensure_ascii=False),
                    characteristics=app_json,
                    variations='[]',
                    variation_attributes='[]',
                    variation_colors=color_json,
                    todays_deal=1,
                    published=1,
                    featured=1,
                    unit='pcs',
                    weight=float(ves)/1000,
                    num_of_sale=0,
                    meta_title=pro_name,
                    meta_description=description,
                    meta_img='',
                    pdf='',
                    slug=elem_slug,
                    earn_point=random.randint(20,100)*100,
                    rating=random.randint(0,5),
                    barcode=papka,
                    digital=1,
                    file_name='',
                    file_path='',
                    created_at='2021-06-28 08:43:07',
                    updated_at='2021-06-28 08:43:07',
                    on_moderation=0,
                    is_accepted=1,
                    refundable=1,
                )
                element_qosh.save()
                self.elem_translation(element_qosh.id,ann,description)
                variation = Variations(
                    name=var_a,
                    lowest_price_id=0,
                    slug=elem_slug,
                    partnum=papka,
                    element_id=element_qosh.id,
                    prices=random.randint(1,10)*100,
                    variant='',
                    description=description,
                    short_description=json.dumps(oxirgi,ensure_ascii=False),
                    created_at='2021-08-01 16:32:32',
                    updated_at='2021-08-01 16:32:32',
                    user_id=9,
                    num_of_sale=0,
                    qty=0,
                    rating=random.randint(0,5),
                    thumbnail_img=photo_thum_json,
                    photos=photo_id_json,
                    color_id=color_id,
                    characteristics=None,
                    deleted_at=None,
                )
                variation.save()
                self.var_translation(variation.id,var_a)
                sel = [3, 52, 69]
                pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                for i in range(0, 3):
                    var_a1 = var_a + pro_names[i]
                    pro_slug = self.get_slugify(f'{var_a1}')
                    if int(self.slug_unique_for_product(pro_slug)) != 0:
                        pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                    p=Products(
                        name=var_a1,
                        slug=pro_slug,
                        user_id=sel[i],
                        added_by='seller',
                        currency_id=1,
                        price=random.randint(1,10)*100,
                        discount=random.randint(0,10),
                        discount_type='percent',
                        discount_start_date=None,
                        discount_end_date=None,
                        variation_id=variation.id,
                        todays_deal=1,
                        num_of_sale=15,
                        delivery_type='tarif',
                        qty=10,
                        est_shipping_days=None,
                        low_stock_quantity=None,
                        published=1,
                        approved=1,
                        stock_visibility_state='quantity',
                        cash_on_delivery=1,
                        tax=random.randint(1,10),
                        tax_type='percent',
                        created_at='2021-09-13 20:22:42',
                        updated_at='2021-09-13 20:22:42',
                        featured=1,
                        seller_featured=0,
                        refundable=1,
                        on_moderation=0,
                        is_accepted=1,
                        digital=0,
                        rating=random.randint(0,5),
                        barcode=papka,
                        earn_point=random.randint(20,100)*100,
                        element_id=element_qosh.id,
                        sku=None,
                        deleted_at=None,
                        is_quantity_multiplied=0
                    ).save()
            else:
                bran_rr_id=Branches.objects.filter(name="Память")[:1].get().id
                Attributes.objects.filter(Q(name="Объем встроенной памяти (Гб)") & Q(branch_id=bran_rr_id)).update(combination=1)
                elem_id = Elements.objects.filter(Q(name=ann) & Q(category_id=category_iddd) & Q(brand_id=brand_id))[:1].get().id
                variat_json = Elements.objects.filter(id=elem_id)[:1].get().variations
                var_json_colors=Elements.objects.filter(id=elem_id)[:1].get().variation_colors
                element_characters=json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                new_rel=self.join_dicts(attr_diction_umumiy,element_characters)
                new_char=new_rel['umumiy']
                if len(new_rel['atr_combinations']):
                    for a in new_rel['atr_combinations']:
                        Attributes.objects.filter(id=a).update(combination=1)

                Elements.objects.filter(id=elem_id).update(characteristics=json.dumps(new_char))
                if var_json_colors!=None:
                    variation_colors=json.loads(var_json_colors)
                else:
                    variation_colors=None
                if color !='':
                    color_id = Colors.objects.filter(name=color)[:1].get().id
                else:
                    color_id=None

                rangi = False
                if color_id !=None:
                    if variation_colors==None:
                        variation_colors=list()
                        variation_colors.append(f'{color_id}')
                    elif f'{color_id}' not in variation_colors:
                        variation_colors.append(f'{color_id}')
                        rangi = True
                    variat_json_color1=json.dumps(variation_colors)
                    variat_json_color=self.remove_space(variat_json_color1)
                    Elements.objects.filter(id=elem_id).update(variation_colors=variat_json_color)
                if memory !="":
                    attri_id = Attributes.objects.filter(Q(name="Объем встроенной памяти (Гб)") & Q(branch_id=bran_rr_id))[:1].get().id
                    memory_id = Characteristics.objects.filter(Q(name=f"{self.remove_all_spaces(memory.lower())}")&Q(attribute_id=attri_id))[:1].get().id
                else:
                    memory_id=None
                if Variations.objects.filter(Q(element_id=elem_id) &Q(color_id=color_id)&Q(characteristics=memory_id)).exists():
                    continue
                if variat_json =='[]':
                    m_dict = {}
                    m_list = []
                    m1 = []
                    if memory != "":
                        m_list.append(f'{memory_id}')
                        m_dict[f'{attri_id}'] = m_list
                        print(f'{variat_json}---keyin----{m_list}')
                        m1.append(f'{attri_id}')
                        a2 = json.dumps(m_dict)
                        m2 = json.dumps(m1)
                        print(f'a2={a2} -----m2={m2} ')
                        elem_char_m=json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                        aa1=list(elem_char_m[f'{attri_id}'])
                        if f'{memory_id}' not in aa1:
                            aa1.append(f'{memory_id}')
                        elem_char_m[f'{attri_id}']=aa1
                        aa2=json.dumps(elem_char_m)
                        Elements.objects.filter(id=elem_id).update(characteristics=aa2,variations=a2, variation_attributes=m2)
                else:
                    if memory !="":
                        a1=json.loads(variat_json)
                        if f'{attri_id}' in a1.keys():
                            a2=list(a1[f'{attri_id}'])
                            if f'{memory_id}' not in a2:
                                a2.append(f'{memory_id}')
                                a1[f'{attri_id}']=a2
                                elem_char_m = json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                                aa1 = list(elem_char_m[f'{attri_id}'])
                                if f'{memory_id}' not in aa1:
                                    aa1.append(f'{memory_id}')
                                elem_char_m[f'{attri_id}'] = aa1
                                aa2 = json.dumps(elem_char_m)
                                Elements.objects.filter(id=elem_id).update(characteristics=aa2,variations=json.dumps(a1))
                        elif f'{attri_id}' not in a1.keys():
                            d=[]
                            for aak in a1.keys():
                                d.append(f'{aak}')
                            elem_char_m = json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                            aa1 = list(elem_char_m[f'{attri_id}'])
                            if f'{memory_id}' not in aa1:
                                aa1.append(f'{memory_id}')
                            elem_char_m[f'{attri_id}'] = aa1
                            aa2 = json.dumps(elem_char_m)
                            a1[f'{attri_id}']=list(f'{memory_id}')
                            Elements.objects.filter(id=elem_id).update(characteristics=aa2,variations=json.dumps(a1),variation_attributes=json.dumps(d))

                phot_list=''
                photo_thum=''

                if not Variations.objects.filter(name=var_name).exists():
                    for i in range(1, 50):
                        if os.path.isfile(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg'):
                            file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')

                            if not Uploads.objects.filter(file_original_name=f'{papka}-{i}').exists():
                                file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{i}.jpg')
                                b_name1 = 'variation'
                                photos_id = self.uploads(f'{papka}-{i}', file_name, file_size, b_name1)
                            else:
                                photos_id = Uploads.objects.filter(file_original_name=f'{papka}-{i}')[:1].get().id

                            if i == 1:
                                photo_thum+=f'{photos_id}'
                                ranglar = ''
                                if rangi:
                                    ranglar = Elements.objects.filter(id=elem_id)[:1].get().photos
                                    a_rrr = ranglar.split(',')
                                    a_rrr.append(f'{photos_id}')
                                    r_hamma = f'{a_rrr[0]}'
                                    for rr in a_rrr[1:]:
                                        r_hamma += f',{rr}'
                                    Elements.objects.filter(id=elem_id).update(photos=r_hamma)
                            else:
                                if i==2:
                                    phot_list+=f'{photos_id}'
                                else:
                                    phot_list+=f',{photos_id}'
                        else:
                            break
                    phot_list_json=phot_list
                    photo_thum_json=photo_thum
                    var_slug=self.get_slugify(f'{var_name}')
                    if int(self.slug_unique_for_var(var_slug))!=0:
                        var_slug=var_slug+f'-{int(self.slug_unique_for_var(var_slug))}'

                    if memory =="":
                        variation = Variations(
                            name=var_name,
                            lowest_price_id=0,
                            slug=var_slug,
                            partnum=papka,
                            element_id=elem_id,
                            prices=random.randint(1,10)*100,
                            variant='',
                            description=description,
                            short_description=json.dumps(oxirgi,ensure_ascii=False),
                            created_at='2021-08-01 16:32:32',
                            updated_at='2021-08-01 16:32:32',
                            user_id=9,
                            num_of_sale=random.randint(1,100),
                            qty=0,
                            rating=random.randint(0,5),
                            thumbnail_img=photo_thum_json,
                            photos=phot_list_json,
                            color_id=color_id,
                            characteristics=None,
                            deleted_at=None,
                        )
                        variation.save()
                        self.var_translation(variation.id, var_name)
                        sel = [3, 52, 69]
                        pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                        for i in range(0, 3):
                            var_a1 = var_name + pro_names[i]
                            pro_slug = self.get_slugify(f'{var_name}')
                            if int(self.slug_unique_for_product(pro_slug)) != 0:
                                pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                            p = Products(
                                name=var_a1,
                                slug=pro_slug,
                                user_id=sel[i],
                                added_by='seller',
                                currency_id=1,
                                price=random.randint(1, 10) * 100,
                                discount=random.randint(0, 10),
                                discount_type='percent',
                                discount_start_date=None,
                                discount_end_date=None,
                                variation_id=variation.id,
                                todays_deal=1,
                                num_of_sale=15,
                                delivery_type='tarif',
                                qty=10,
                                est_shipping_days=None,
                                low_stock_quantity=None,
                                published=1,
                                approved=1,
                                stock_visibility_state='quantity',
                                cash_on_delivery=1,
                                tax=random.randint(1, 10),
                                tax_type='percent',
                                created_at='2021-09-13 20:22:42',
                                updated_at='2021-09-13 20:22:42',
                                featured=1,
                                seller_featured=0,
                                refundable=1,
                                on_moderation=0,
                                is_accepted=1,
                                digital=0,
                                rating=random.randint(0, 5),
                                barcode=papka,
                                earn_point=random.randint(20, 100) * 100,
                                element_id=elem_id,
                                sku=None,
                                deleted_at=None,
                                is_quantity_multiplied=0
                            ).save()


                    else:
                        memory_id1 = Characteristics.objects.filter(name=f"{self.remove_all_spaces(memory.lower())}")[:1].get().id
                        print(f'memory_id={memory_id1}')
                        variation = Variations(
                            name=var_name,
                            lowest_price_id=0,
                            slug=var_slug,
                            partnum=papka,
                            element_id=elem_id,
                            prices=random.randint(1,10)*100,
                            variant='',
                            description=description,
                            short_description=json.dumps(oxirgi,ensure_ascii=False),
                            created_at='2021-08-01 16:32:32',
                            updated_at='2021-08-01 16:32:32',
                            user_id=9,
                            num_of_sale=random.randint(1,100),
                            qty=0,
                            rating=random.randint(0,5),
                            thumbnail_img=photo_thum_json,
                            photos=phot_list_json,
                            color_id=color_id,
                            characteristics=memory_id1,
                            deleted_at=None,
                        )
                        variation.save()
                        self.var_translation(variation.id, var_name)
                        sel = [3, 52, 69]
                        pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                        for i in range(0, 3):
                            var_a1 = var_name + pro_names[i]
                            pro_slug = self.get_slugify(f'{var_a1}')
                            if int(self.slug_unique_for_product(pro_slug)) != 0:
                                pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                            p = Products(
                                name=var_a1,
                                slug=pro_slug,
                                user_id=sel[i],
                                added_by='seller',
                                currency_id=1,
                                price=random.randint(1, 10) * 100,
                                discount=random.randint(0, 10),
                                discount_type='percent',
                                discount_start_date=None,
                                discount_end_date=None,
                                variation_id=variation.id,
                                todays_deal=1,
                                num_of_sale=15,
                                delivery_type='tarif',
                                qty=10,
                                est_shipping_days=None,
                                low_stock_quantity=None,
                                published=1,
                                approved=1,
                                stock_visibility_state='quantity',
                                cash_on_delivery=1,
                                tax=random.randint(1, 10),
                                tax_type='percent',
                                created_at='2021-09-13 20:22:42',
                                updated_at='2021-09-13 20:22:42',
                                featured=1,
                                seller_featured=0,
                                refundable=1,
                                on_moderation=0,
                                is_accepted=1,
                                digital=0,
                                rating=random.randint(0, 5),
                                barcode=papka,
                                earn_point=random.randint(20, 100) * 100,
                                element_id=elem_id,
                                sku=None,
                                deleted_at=None,
                                is_quantity_multiplied=0
                            ).save()




tag_list = [
'Аккумулятор для мобильного телефона',
'Дисплей для планшета',
'Дисплей для смартфона',
'Запчасть для мобильного телефона',
'Присоска для снятия дисплея',
'Скрепка для сим-карты',
'Тачскрин для планшета',
'Тачскрин для смартфона'

]

class Command(BaseCommand):
    help='Parsing Wildberries'
    def handle(self, *args, **options):
        p=WildberiesParser()
        # p.get_dict('Ноутбуки','https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki',7,'Ноутбук',tag_list)

        # p.get_dict_d('Ноутбуки', 'https://www.wildberries.ru/catalog/elektronika/noutbuki-pereferiya/noutbuki-ultrabuki', 7,tag_list)
        p.get_path_d('Запчасти для устройств', 200, tag_list)



 # p.put_branch(cate_name={'Планшеты': 'https://www.wildberries.ru/catalog/elektronika/planshety'},number=2)






