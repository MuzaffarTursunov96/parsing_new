import time
from collections import namedtuple
from bs4 import  BeautifulSoup
import  requests
import os
import socket
import socks
import ast
from slugify import slugify
import shutil
import json
from parse.models import AttributeCategory,AttributeTranslations,Attributes,BranchTranslations,Branches,BrandTranslations,Brands,Categories,CategoryTranslations,CharacteristicTranslations,Characteristics,ColorTranslations,Colors,ElementTranslations,Elements,Products,Uploads,VariationTranslations,Variations,BrandCategory
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
import argon2, binascii
import random
from django.db.models import Q

all_dictionary = {
    'Смартфоны': 'https://www.wildberries.ru/catalog/elektronika/smartfony-i-telefony/vse-smartfony'
}



class Parse_All:
    def check_exists(self, cate_name, prod_name):
        absolute_path = os.path.abspath(__file__)
        filees = os.path.isfile(f'{os.path.dirname(absolute_path)}\{cate_name}\{prod_name}\product_detail.html')
        return filees
    def check_exists_d(self, name11,name22,papka):
        absolute_path = os.path.abspath(__file__)
        filees = os.path.isfile(f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\product_detail.html')
        return filees

    def get_category_and_link(self):
        absolute_path = os.path.abspath(__file__)
        category_0_list = []
        category_1_list = []
        category_2_list = []
        category_2_dict_link={}
        category_3_list = []
        ############ get category 0 ids
        for cate_0 in Categories.objects.filter(level=0):
            category_0_list.append(cate_0.id)
        ########## get category 1 ids
        for cate_0 in category_0_list:
            cate_00=Categories.objects.filter(parent_id=cate_0)
            for cate_000 in cate_00:
                category_1_list.append(cate_000.id)
        ############# get category 2 ids
        for cate_1 in category_1_list:
            cate_11=Categories.objects.filter(parent_id=cate_1)
            for cate_111 in cate_11:
                cate_2_id =cate_111.id
                cate_2_link =cate_111.link
                category_2_dict_link[f'{cate_2_id}']=f'{cate_2_link}'
                category_2_list.append(cate_2_id)
        only_2={}
        only_3={}
        for cate_2 in category_2_list:
            if not Categories.objects.filter(parent_id=cate_2).exists():
                if Categories.objects.filter(id=cate_2)[:1].get().link!=None:
                    only_2[cate_2]=Categories.objects.filter(id=cate_2)[:1].get().link
            else:
                only_33={}
                for c in Categories.objects.filter(parent_id=cate_2).all():
                    if ('brand' not in str(c.link))and(c.link!=None):
                        only_33[c.id]=c.link
                        only_3[cate_2]=only_33
        if not os.path.isfile(f"{os.path.dirname(absolute_path)}\category_two.json"):
            with open(f"{os.path.dirname(absolute_path)}\category_two.json", 'w',
                      encoding='utf-8') as file:
                json.dump(only_2, file, indent=4, ensure_ascii=False)
        if not os.path.isfile(f"{os.path.dirname(absolute_path)}\category_three.json"):
            with open(f"{os.path.dirname(absolute_path)}\category_three.json", 'w',
                      encoding='utf-8') as file:
                json.dump(only_3, file, indent=4, ensure_ascii=False)

        # print(only_3)







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


    def html_yaratish(self, res, cat_name, prod_name):
        absolute_path = os.path.abspath(__file__)
        with open(f"{os.path.dirname(absolute_path)}\{cat_name}\{prod_name}\product_detail.html", 'w',
                  encoding='utf-8') as file:
            file.write(res)

    def cate_dir(self, name):
        absolute_path = os.path.abspath(__file__)
        parent_dir = f'{os.path.dirname(absolute_path)}'
        path = os.path.join(parent_dir, f'{name}')
        os.mkdir(path)

    def cate_dir_d(self,name1, name2):
        absolute_path = os.path.abspath(__file__)
        parent_dir = f'{os.path.dirname(absolute_path)}\{name1}'
        path = os.path.join(parent_dir, f'{name2}')
        os.mkdir(path)

    def get_dict(self,num,num_product):
        absolute_path = os.path.abspath(__file__)
        categories_2 = self.read_json(f"{os.path.dirname(absolute_path)}\category_two.json")
        for name_id, link in categories_2.items():
            if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name_id}'):
                self.cate_dir(name_id)
            for i in range(1,num+1):
                if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{name_id}\{i}.html'):
                    response = self.get_html(f'{link}')
                    time.sleep(3)
                    source = response.text
                    with open(f"{os.path.dirname(absolute_path)}\{name_id}\{i}.html", 'w', encoding='utf-8') as file:
                        file.write(source)
            self.get_path_c(num,name_id,num_product)

    def get_dict_d(self,num,num_product):
        absolute_path = os.path.abspath(__file__)
        categories_3_2 = self.read_json(f"{os.path.dirname(absolute_path)}\category_three.json")

        for name_id_1,dat in categories_3_2.items():
            for name_id_2, link in dat.items():
                if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name_id_1}'):
                    self.cate_dir(name_id_1)
                if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name_id_1}\{name_id_2}'):
                    self.cate_dir_d(name_id_1,name_id_2)
                for i in range(1,num+1):
                    if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{name_id_1}\{name_id_2}\{i}.html'):
                        response = self.get_html(f'{link}')
                        time.sleep(3)
                        source = response.text
                        with open(f"{os.path.dirname(absolute_path)}\{name_id_1}\{name_id_2}\{i}.html", 'w', encoding='utf-8') as file:
                            file.write(source)
                self.get_path_d(num,name_id_1,name_id_2,num_product)


    def nom(self, product_href):
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

    def prod_papka_yaratish_c(self, cate_name, nomi):
        absolute_path = os.path.abspath(__file__)
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{cate_name}\{nomi}'):
            return True
        else:
            return False
    def prod_papka_yaratish_d(self, nomi1,nomi2,papka ):
        absolute_path = os.path.abspath(__file__)
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{nomi1}\{nomi2}\{papka}'):
            return True
        else:
            return False
    def check_img_dir_d(self, name11,name22, papka, images):
        absolute_path = os.path.abspath(__file__)
        if os.path.isdir(f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\{images}'):
            return True
        else:
            return False
    def check_img_dir(self, name1, papka, images):
        absolute_path = os.path.abspath(__file__)
        if os.path.isdir(f'{os.path.dirname(absolute_path)}\{name1}\{papka}\{images}'):
            return True
        else:
            return False
    def get_html(self, url):
        response = self.test_request(url)
        if 'Requests quota exceeded' in response.text:
            time.sleep(60)
            return self.get_html(url)
        return response

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
                self.product_css_c(source, cate_22,num_pro)
                self.product_characters_cc(source, cate_22,num_pro)
                self.product_attributes_c(source,cate_22)
                self.put_elements_c(source,cate_22,num_pro)
                print(cate_22)
                # self.product_css_d(source,cate_22, cate_222.id)
                # self.product_characters_dc(source,cate_22,cate_222.id)
            # except ObjectDoesNotExist as ex:
            #     for i in range(1, 2):
            #         with open(f"{os.path.dirname(absolute_path)}\{cate_22}\{i}.html", encoding='utf-8') as file:
            #             source = file.read()

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
                self.product_css_d(source, cate_11,cate_22,num_pro)
                self.product_characters_dd(source, cate_11,cate_22,num_pro)
                self.product_attributes_d(source,cate_11,cate_22)
                self.put_elements_d(source,cate_11,cate_22,num_pro)
            print(cate_22)


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

    def product_css_c(self, source, name,number_of_prod):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        x=0
        for product_hrefs in all_product:
            if int(x)==int(number_of_prod):
                break
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            print(papka)
            absolute_path = os.path.abspath(__file__)
            if self.prod_papka_yaratish_c(name, papka):
                parent_dir = f'{os.path.dirname(absolute_path)}\{name}'
                path = os.path.join(parent_dir, f'{papka}')
                os.mkdir(path)
                par_img = f'{os.path.dirname(absolute_path)}\{name}\{papka}'
                if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name}\{papka}\images'):
                    path_img = os.path.join(par_img, 'images')
                    os.mkdir(path_img)
            if self.check_exists(name, papka):
                x+= 1
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
            x += 1

    def product_css_d(self, source, name1,name2,number_of_prod):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        x=0

        for product_hrefs in all_product:
            if int(x)==int(number_of_prod):
                break
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            print(papka)
            absolute_path = os.path.abspath(__file__)
            if self.prod_papka_yaratish_d(name1,name2, papka):
                parent_dir = f'{os.path.dirname(absolute_path)}\{name1}\{name2}'
                path = os.path.join(parent_dir, f'{papka}')
                os.mkdir(path)
                par_img = f'{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}'
                if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\images'):
                    path_img = os.path.join(par_img, 'images')
                    os.mkdir(path_img)
            if self.check_exists_d(name1,name2,papka):
                x+= 1
                continue
            else:
                response1 = self.get_html(f'https://www.wildberries.ru{product_href}')
                source1 = response1.text
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\product_detail.html", 'w',
                          encoding='utf-8') as file:
                    file.write(source1)

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\product_detail.html",
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
                product_brand_name = self.replace_drop(product_brand_name1)

            if brand_img_href != None:
                brand1 = self.test_request(f'https:{brand_img_href}')
                brand = brand1.content
                b_name = product_brand_name
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\images\{b_name}.jpg",
                          'wb') as file:
                    file.write(brand)
                brand_name = 'brand'
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\{brand_name}.json", 'w',
                          encoding='utf-8') as file:
                    json.dump(product_brand_name, file, indent=4, ensure_ascii=False)

            if self.check_img_dir_d(name1,name2,papka, 'images'):
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
                                f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\images\{papka}-{count_img}.jpg",'wb') as file:
                            file.write(req_img)
                        count_img += 1

            x += 1


    def product_characters_cc(self, source, name1,number_product):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        x=0
        for product_hrefs in all_product:
            if x==number_product:
                break
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

            # print(source.find(class_='same-part-kt__color').find('span'))
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
                            sub_cap_dict[f'{sub_name}'] = f'{sub_value}'
                        else:
                            continue

                cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'

            else:
                for a in source.find(class_='product-params').find(class_='product-params__table').find_all('tbody'):
                    sub_name = a.find('tr').find('th').find('span').find('span').get_text()
                    sub_val = a.find('tr').find('td').get_text()
                    sub_value = sub_val.split(';')
                    sub_cap_dict[f'{sub_name}'] = f'{sub_value}'
                cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'

            descrip = {}
            for desc in source.find_all(class_='product-detail__details details'):
                description_title = desc.find('h2').get_text()
                description_text = desc.find(class_='details__content').find('p').get_text()
                descrip[f'{description_title}'] = f'{description_text}'
            descrip['color'] = f'{color}'

            if source.find(class_='same-part-kt__show-sizes'):
                size_list = []
                for size in source.find(class_='same-part-kt__sizes-list').find_all(class_='sizes-list__item'):
                    if size.find('label').find(class_='sizes-list__size-ru')!=None:
                        size_val = size.find('label').find(class_='sizes-list__size-ru').get_text()
                    elif size.find('label').find(class_='sizes-list__size')!=None:
                        size_val = size.find('label').find(class_='sizes-list__size').get_text()
                    size_list.append(size_val)
                if size_list[0]!='':
                    szxx=[]
                    szxx.append(f'{size_list[0]}')
                    sub_cap_dict['Размер'] = f'{szxx}'
                    cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'
                    with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\sizes.json", 'w',
                              encoding='utf-8') as file:
                        json.dump(size_list, file, indent=4, ensure_ascii=False)

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\description.json", 'w',
                      encoding='utf-8') as file:
                json.dump(descrip, file, indent=4, ensure_ascii=False)

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\product_characters.json", 'w',
                      encoding='utf-8') as file:
                json.dump(cap_dict, file, indent=4, ensure_ascii=False)
            x+=1

    def product_characters_dd(self, source, name1,name2,number_product):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        x=0
        for product_hrefs in all_product:
            if x==number_product:
                break
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            try:
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\product_detail.html",
                          encoding='utf-8') as file:
                    soup = file.read()
            except FileNotFoundError as ex:
                continue

            source = BeautifulSoup(soup, 'lxml')
            try:
                caption = source.find(class_='product-params').find(class_='product-params__table').find('caption')
            except AttributeError as ex:
                continue
            
            # print(source.find(class_='same-part-kt__color').find('span'))
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
                            sub_cap_dict[f'{sub_name}'] = f'{sub_value}'
                        else:
                            continue

                cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'

            else:
                for a in source.find(class_='product-params').find(class_='product-params__table').find_all('tbody'):
                    sub_name = a.find('tr').find('th').find('span').find('span').get_text()
                    sub_val = a.find('tr').find('td').get_text()
                    sub_value = sub_val.split(';')
                    sub_cap_dict[f'{sub_name}'] = f'{sub_value}'
                cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'

            descrip = {}
            for desc in source.find_all(class_='product-detail__details details'):
                description_title = desc.find('h2').get_text()
                description_text = desc.find(class_='details__content').find('p').get_text()
                descrip[f'{description_title}'] = f'{description_text}'
            descrip['color'] = f'{color}'

            if source.find(class_='same-part-kt__show-sizes'):
                size_list = []
                for size in source.find(class_='same-part-kt__sizes-list').find_all(class_='sizes-list__item'):
                    if size.find('label').find(class_='sizes-list__size-ru')!=None:
                        size_val = size.find('label').find(class_='sizes-list__size-ru').get_text()
                    elif size.find('label').find(class_='sizes-list__size')!=None:
                        size_val = size.find('label').find(class_='sizes-list__size').get_text()
                    size_list.append(size_val)
                if size_list[0]!='':
                    szxx=[]
                    szxx.append(f'{size_list[0]}')
                    sub_cap_dict['Размер'] = f'{szxx}'
                    cap_dict[f'{caption_name}'] = f'{sub_cap_dict}'
                    with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\sizes.json", 'w',
                              encoding='utf-8') as file:
                        json.dump(size_list, file, indent=4, ensure_ascii=False)

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\description.json", 'w',
                      encoding='utf-8') as file:
                json.dump(descrip, file, indent=4, ensure_ascii=False)

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\product_characters.json", 'w',
                      encoding='utf-8') as file:
                json.dump(cap_dict, file, indent=4, ensure_ascii=False)
            x+=1


    def get_slugify(self,name):
        return slugify(f'{name}', to_lower=True)


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


    def attribute_translation(self,attr_id,name):
        for i in range(1, 4):
            if i == 1:
                lang = 'en'
            elif i==2:
                lang ='ru'
            elif i==3:
                lang='uz'
            p=AttributeTranslations(
                attribute_id=attr_id,
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


    def get_attributes(self,name):
        attribute_id=Attributes.objects.filter(name=name)[:1].get().id
        return attribute_id



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
                    self.put_category_and_attr(int(category_name_id), attr_id)

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
                                # self.attr_charakteristic(attribute_id, char_id)
                                self.char_translation(char_id, name=cha_rem)

            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\sizes.json"):
                single_branch_name = list(json_data.keys())[-1]
                if not Branches.objects.filter(name=single_branch_name).exists():
                    branch__tt = Branches(
                        name=single_branch_name,
                        created_at='2021-07-01 17:44:48',
                        updated_at='2021-07-18 07:51:00',
                    )
                    branch__tt.save()
                    id = branch__tt.id
                    self.branch_translation(id, name=single_branch_name)
                else:
                    id = Branches.objects.filter(name=single_branch_name)[:1].get().id

                if not Attributes.objects.filter(Q(branch_id=id) & Q(name='Размер')).exists():
                    atributess = Attributes(
                        branch_id=id,
                        name='Размер',
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
                self.put_category_and_attr(category_name_id, attr_id)

                xx = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\sizes.json")
                for char_val in range(0, len(xx)):
                    cha_rem = self.remove_all_spaces(xx[char_val].lower())
                    if ((cha_rem != '') and (cha_rem != '-')):
                        if not Characteristics.objects.filter(Q(name=cha_rem) & Q(attribute_id=attr_id)).exists():
                            slug = self.get_slugify(f'{cha_rem}')
                            if int(self.slug_unique_for_chars(slug)) != 0:
                                slug = slug + f'-{int(self.slug_unique_for_chars(slug))}'
                            pch = Characteristics(
                                attribute_id=attr_id,
                                name=cha_rem,
                                slug=slug,
                                created_at='2021-05-29 00:55:49',
                                updated_at='2021-05-20 21:05:09',
                                deleted_at=None,
                            )
                            pch.save()
                            char_id = pch.id
                            # self.attr_charakteristic(attribute_id, char_id)
                            self.char_translation(char_id, name=cha_rem)

            brand_n = 'brand'
            a = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id}\{papka}\{brand_n}.json")
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
            cater_id =category_name_id
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


    def product_attributes_d(self, source, category_name_id_1,category_name_id_2):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            try:
                json_data = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id_1}\{category_name_id_2}\{papka}\product_characters.json")
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
                    self.put_category_and_attr(int(category_name_id_1), attr_id)

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
                                # self.attr_charakteristic(attribute_id, char_id)
                                self.char_translation(char_id, name=cha_rem)

            if os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name_id_1}\{category_name_id_2}\{papka}\sizes.json"):
                single_branch_name = list(json_data.keys())[-1]
                if not Branches.objects.filter(name=single_branch_name).exists():
                    branch__tt = Branches(
                        name=single_branch_name,
                        created_at='2021-07-01 17:44:48',
                        updated_at='2021-07-18 07:51:00',
                    )
                    branch__tt.save()
                    id = branch__tt.id
                    self.branch_translation(id, name=single_branch_name)
                else:
                    id = Branches.objects.filter(name=single_branch_name)[:1].get().id

                if not Attributes.objects.filter(Q(branch_id=id) & Q(name='Размер')).exists():
                    atributess = Attributes(
                        branch_id=id,
                        name='Размер',
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
                self.put_category_and_attr(category_name_id_1, attr_id)

                xx = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id_1}\{category_name_id_2}\{papka}\sizes.json")
                for char_val in range(0, len(xx)):
                    cha_rem = self.remove_all_spaces(xx[char_val].lower())
                    if ((cha_rem != '') and (cha_rem != '-')):
                        if not Characteristics.objects.filter(Q(name=cha_rem) & Q(attribute_id=attr_id)).exists():
                            slug = self.get_slugify(f'{cha_rem}')
                            if int(self.slug_unique_for_chars(slug)) != 0:
                                slug = slug + f'-{int(self.slug_unique_for_chars(slug))}'
                            pch = Characteristics(
                                attribute_id=attr_id,
                                name=cha_rem,
                                slug=slug,
                                created_at='2021-05-29 00:55:49',
                                updated_at='2021-05-20 21:05:09',
                                deleted_at=None,
                            )
                            pch.save()
                            char_id = pch.id
                            # self.attr_charakteristic(attribute_id, char_id)
                            self.char_translation(char_id, name=cha_rem)

            brand_n = 'brand'
            a = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id_1}\{category_name_id_2}\{papka}\{brand_n}.json")
            if a[-1:] == '.':
                product_brand_nam = a.replace('.', '')
            else:
                product_brand_nam = a

            if '/' in product_brand_nam:
                b_name = product_brand_nam.replace('/', '')
            else:
                b_name = product_brand_nam

            file_size = os.path.getsize(f"{os.path.dirname(absolute_path)}\{category_name_id_1}\{category_name_id_2}\{papka}\images\{b_name}.jpg")
            if not Uploads.objects.filter(file_original_name=b_name).exists():
                file_name = self.hash_and_move(b_name,f"{os.path.dirname(absolute_path)}\{category_name_id_1}\{category_name_id_2}\{papka}\images\{b_name}.jpg")
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
            cater_id =category_name_id_1
            brand_id = Brands.objects.filter(name=f"{b_name}")[:1].get().id
            if not BrandCategory.objects.filter(Q(brand_id=brand_id) & Q(category_id=cater_id)).exists():
                BrandCategory(
                    brand_id=brand_id,
                    category_id=cater_id
                ).save()
            color = self.read_json(f"{os.path.dirname(absolute_path)}\{category_name_id_1}\{category_name_id_2}\{papka}\description.json")['color']
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



    def read_file(self,path):
        file = open(path, "r",encoding='utf-8')
        data = file.read()
        file.close()
        return data


    def uploads(self,name,file_name,file_size,t_name):
        n='all'
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

    def put_category_and_attr(self, category_id, atr_id):
        if not AttributeCategory.objects.filter(Q(attribute_id=f'{atr_id}') & Q(category_id=int(category_id))).exists():
            p = AttributeCategory(
                attribute_id=atr_id,
                category_id=category_id
            ).save()

    def slug_unique_for_var(self, slug):
        if Variations.objects.filter(slug__startswith=slug).exists():
            a = Variations.objects.filter(slug__startswith=slug).count()
            print(Variations.objects.filter(slug__startswith=slug)[:1].get().slug)
            return a
        else:
            return 0

    def slug_unique_for_chars(self, slug):
        if Characteristics.objects.filter(slug__startswith=slug).exists():
            a = Characteristics.objects.filter(slug__startswith=slug).count()
            print(Characteristics.objects.filter(slug__startswith=slug)[:1].get().slug)
            return a
        else:
            return 0

    def slug_unique_for_elem(self, slug):
        if Elements.objects.filter(slug__startswith=slug).exists():
            a = Elements.objects.filter(slug__startswith=slug).count()
            print(Elements.objects.filter(slug__startswith=slug)[:1].get().slug)
            return a
        else:
            return 0

    def slug_unique_for_brand(self, slug):
        if Brands.objects.filter(slug__startswith=slug).exists():
            a = Brands.objects.filter(slug__startswith=slug).count()
            print(Brands.objects.filter(slug__startswith=slug)[:1].get().slug)
            return a
        else:
            return 0


    def slug_unique_for_product(self, slug):
        if Products.objects.filter(slug__startswith=slug).exists():
            a = Products.objects.filter(slug__startswith=slug).count()
            print(Products.objects.filter(slug__startswith=slug)[:1].get().slug)
            return a
        else:
            return 0

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

            name = 'brand'
            if not (os.path.exists(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\{name}.json") and os.path.getsize(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\{name}.json") != 0):
                continue
            bran = self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\{name}.json")
            if bran[-1:] == '.':
                brand = bran.replace('.', '')
            else:
                brand = bran
            if '/' in brand:
                brand = brand.replace('/', '')

            brand_id=Brands.objects.filter(name=brand)[:1].get().id

            description = mal['Описание']
            json_data = self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\product_characters.json")
            attr_diction_umumiy = {}
            ves = 0
            branch_list = []
            for name, values in json_data.items():
                branch_1_dict = {}
                branch1_id = Branches.objects.filter(name=name)[:1].get().id
                branch_1_dict['id'] = branch1_id
                branch_1_dict['title'] = f'{name}'
                res = ast.literal_eval(values)
                atrd_list = []
                for sub_name, sub_value in res.items():
                    attribute_dict = {}
                    charak_list = []
                    if sub_name == 'Вес товара с упаковкой (г)':
                        ves = int(float(sub_value.replace('[', '').replace(']', '').replace(' ', '').replace('г', '').replace("'","")))
                    char_dict = ast.literal_eval(sub_value)
                    # print(f'branch_id=== {branch1_id}----------------attribute name={sub_name}')
                    attri_id = Attributes.objects.filter(Q(name=sub_name) & Q(branch_id=branch1_id))[:1].get().id
                    attribute_dict['id'] = attri_id
                    attribute_dict['attribute'] = f'{sub_name}'
                    char_l = []
                    for char in char_dict:
                        char_name = self.remove_all_spaces(char.lower())
                        if ((char_name != '') and (char_name != '-')):
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
                            c_a = {}
                            ggg = str(char_id)
                            c_a['id'] = int(ggg.replace('(),', ''))
                            c_a['name'] = f'{char_name}'
                            char_l.append(c_a)
                            # try:
                            #     attr_chars_id=AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=char_id)[:1].get().id
                            # except ObjectDoesNotExist as den:
                            #     p=AttributeCharacteristic(
                            #         attribute_id=attri_id,
                            #         characteristic_id=char_id
                            #     ).save()
                            #     attr_chars_id=AttributeCharacteristic.objects.filter(attribute_id=attri_id, characteristic_id=char_id)[:1].get().id
                            #
                            #
                            # if aaa =='':
                            #     aaa+=str(attr_chars_id)
                            # elif aaa !='':
                            #     aaa+=','+str(attr_chars_id)
                    attribute_dict['values'] = char_l
                    atrd_list.append(attribute_dict)
                    attr_diction_umumiy[f'{attri_id}'] = charak_list
                branch_1_dict['options'] = atrd_list
                branch_list.append(branch_1_dict)
            oxirgi = {}
            oxirgi['en'] = branch_list
            oxirgi['ru'] = branch_list
            oxirgi['uz'] = branch_list

            app_json = json.dumps(attr_diction_umumiy)

            co = []
            if color != '':
                color_id = Colors.objects.filter(name=f'{color}')[:1].get().id
                co.append(f'{color_id}')
                color_json = json.dumps(co)
            else:
                color_json = None
                color_id = None

            if not Elements.objects.filter(Q(name=f"{a}") & Q(category_id=name11) & Q(brand_id=brand_id)).exists():
                if color!='':
                    var_a = a+', '+color
                else:
                    var_a = a
                brand_id=Brands.objects.filter(name=f'{brand}')[:1].get().id
                # app_json=aaa


                var_js=''
                photo_thum_list=''
                photo_list = ''
                for i in range(1,50):
                    if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{papka}-{i}.jpg'):
                        break
                    else:
                        file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{papka}-{i}.jpg')
                        if not Uploads.objects.filter(file_original_name=f'{papka}-{i}').exists():
                            file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{papka}-{i}.jpg')
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
                elem_slug=self.get_slugify(f'{a}')
                if int(self.slug_unique_for_elem(elem_slug))!=0:
                    elem_slug = elem_slug + f'-{int(self.slug_unique_for_elem(elem_slug))}'

                element_qosh = Elements(
                    name=a,
                    added_by='admin',
                    user_id=9,
                    category_id=int(name11),
                    parent_id=0,
                    brand_id=brand_id,
                    photos=photo_thum_list,
                    thumbnail_img=photo_thum_json,
                    video_provider='youtube',
                    video_link='',
                    tags='',
                    short_description=json.dumps(oxirgi, ensure_ascii=False),
                    description=description,
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
                    deleted_at=None,
                    on_moderation=0,
                    is_accepted=1,
                    refundable=1,
                )
                element_qosh.save()
                self.elem_translation(element_qosh.id,name=a,des=description)

                var_slug = self.get_slugify(f'{var_a}')
                if int(self.slug_unique_for_var(var_slug)) != 0:
                    var_slug = var_slug + f'-{int(self.slug_unique_for_var(var_slug))}'
                variation = Variations(
                    name=var_a,
                    lowest_price_id=0,
                    slug=var_slug,
                    partnum=papka,
                    element_id=element_qosh.id,
                    prices=random.randint(1,10)*100,
                    short_description=json.dumps(oxirgi, ensure_ascii=False),
                    description=description,
                    variant='',
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

                self.var_translation(variation.id, name=var_a)
                sel = [3, 52, 69]
                pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                for i in range(0, 3):
                    var_a1 = a + pro_names[i]
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

                if os.path.isfile(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\sizes.json"):
                    sizes_list=self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\sizes.json")
                    branchh_idd=Branches.objects.filter(name=name)[:1].get().id
                    last_att=Attributes.objects.filter(Q(branch_id=branchh_idd) & Q(name='Размер'))[:1].get().id
                    element_variation={}
                    sz_list=[]
                    for ss in sizes_list[2:]:
                        charr_id=Characteristics.objects.filter(Q(attribute_id=last_att) & Q(name=ss))[:1].get().id
                        sz_list.append(f'{charr_id}')
                        if color != '':
                            var_a = a + ', ' + ss + ', ' + color
                        else:
                            var_a = a + ', ' + ss

                        var_slug = self.get_slugify(f'{var_a}')
                        if int(self.slug_unique_for_var(var_slug)) != 0:
                            var_slug = var_slug + f'-{int(self.slug_unique_for_var(var_slug))}'
                        variation = Variations(
                            name=var_a,
                            lowest_price_id=0,
                            slug=var_slug,
                            partnum=papka,
                            element_id=element_qosh.id,
                            prices=random.randint(1, 10) * 100,
                            short_description=json.dumps(oxirgi, ensure_ascii=False),
                            description=description,
                            variant='',
                            created_at='2021-08-01 16:32:32',
                            updated_at='2021-08-01 16:32:32',
                            user_id=9,
                            num_of_sale=0,
                            qty=0,
                            rating=random.randint(0, 5),
                            thumbnail_img=photo_thum_json,
                            photos=photo_id_json,
                            color_id=color_id,
                            characteristics=charr_id,
                            deleted_at=None,
                        )
                        variation.save()
                        var_id = variation.id
                        self.var_translation(var_id, name=var_a)
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
                                price=random.randint(1, 10) * 100,
                                discount=random.randint(0, 10),
                                discount_type='percent',
                                discount_start_date=None,
                                discount_end_date=None,
                                variation_id=var_id,
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
                                element_id=element_qosh.id,
                                sku=None,
                                deleted_at=None,
                                is_quantity_multiplied=0
                            ).save()
                    element_variation[f'{last_att}']=sz_list
                    attr_iddd=[]
                    attr_iddd.append(f'{last_att}')
                    Elements.objects.filter(id=element_qosh.id).update(variations=json.dumps(element_variation),variation_attributes=json.dumps(attr_iddd))
            else:
                elem_id = Elements.objects.filter(name=f'{a}')[:1].get().id
                new_variat =json.loads(Elements.objects.filter(id=elem_id)[:1].get().variations)
                new_variat_attri = json.loads(Elements.objects.filter(id=elem_id)[:1].get().variation_attributes)
                var_json_colors = Elements.objects.filter(id=elem_id)[:1].get().variation_colors
                if var_json_colors != None:
                    variation_colors = json.loads(var_json_colors)
                else:
                    variation_colors = None
                if color != '':
                    color_id = Colors.objects.filter(name=f'{color}')[:1].get().id
                else:
                    color_id = None
                rangi=False
                if color_id != None:
                    if variation_colors == None:
                        variation_colors = list()
                        variation_colors.append(f'{color_id}')
                    elif f'{color_id}' not in variation_colors:
                        variation_colors.append(f'{color_id}')
                        rangi=True
                    variat_json_color1 = json.dumps(variation_colors)
                    variat_json_color = self.remove_space(variat_json_color1)
                    Elements.objects.filter(id=elem_id).update(variation_colors=variat_json_color)

                if not os.path.isfile(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\sizes.json"):
                    if color != '':
                        var_name =f'{a}, {color}'
                    else:
                        var_name=a
                    phot_list=''
                    photo_thum=''
                    if not Variations.objects.filter(name=var_name).exists():
                        for i in range(1, 50):
                            if os.path.isfile(f'{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{papka}-{i}.jpg'):
                                file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{papka}-{i}.jpg')
                                if not Uploads.objects.filter(file_original_name=f'{papka}-{i}').exists():
                                    file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{papka}-{i}.jpg')
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

                        variation = Variations(
                            name=var_name,
                            lowest_price_id=0,
                            slug=var_slug,
                            partnum=papka,
                            element_id=elem_id,
                            prices=random.randint(1,10)*100,
                            short_description=json.dumps(oxirgi, ensure_ascii=False),
                            description=description,
                            variant='',
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
                        self.var_translation(variation.id, name=var_name)
                        sel = [3, 52, 69]
                        pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                        for i in range(0, 3):
                            var_a1 = var_name + pro_names[i]
                            pro_slug = self.get_slugify(f'{var_a1}')
                            if int(self.slug_unique_for_product(pro_slug)) != 0:
                                pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                            p=Products(
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
                    sizes_list = self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\sizes.json")
                    brann_idd=Branches.objects.filter(name=name)[:1].get().id
                    last_att = Attributes.objects.filter(Q(branch_id=brann_idd) & Q(name='Размер'))[:1].get().id
                    element_variation = {}
                    sz_list = []
                    phot_list = ''
                    photo_thum = ''
                    x = 0
                    for ss in sizes_list:
                        charr_id = Characteristics.objects.filter(Q(attribute_id=last_att) & Q(name=ss))[:1].get().id
                        sz_list.append(f'{charr_id}')
                        if color != '':
                            var_a = a + ', ' + ss + ', ' + color
                        else:
                            var_a = a + ', ' + ss

                        if not Variations.objects.filter(name=var_a).exists():
                            x+=1
                            if x==1:
                                for i in range(1, 50):
                                    if os.path.isfile(f'{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{papka}-{i}.jpg'):
                                        file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{papka}-{i}.jpg')
                                        if not Uploads.objects.filter(file_original_name=f'{papka}-{i}').exists():
                                            file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{papka}-{i}.jpg')
                                            b_name1='variation'
                                            photos_id = self.uploads(f'{papka}-{i}', file_name, file_size,b_name1)
                                        else:
                                            photos_id=Uploads.objects.filter(file_original_name=f'{papka}-{i}')[:1].get().id

                                        if i == 1:
                                            photo_thum += f'{photos_id}'
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
                                            if i == 2:
                                                phot_list += f'{photos_id}'
                                            else:
                                                phot_list += f',{photos_id}'
                                    else:
                                        break
                                phot_list_json = phot_list
                                photo_thum_json = photo_thum

                            var_slug = self.get_slugify(f'{var_a}')
                            if int(self.slug_unique_for_var(var_slug)) != 0:
                                var_slug = var_slug + f'-{int(self.slug_unique_for_var(var_slug))}'
                            variation = Variations(
                                name=var_a,
                                lowest_price_id=0,
                                slug=var_slug,
                                partnum=papka,
                                element_id=elem_id,
                                prices=random.randint(1, 10) * 100,
                                short_description=json.dumps(oxirgi, ensure_ascii=False),
                                description=description,
                                variant='',
                                created_at='2021-08-01 16:32:32',
                                updated_at='2021-08-01 16:32:32',
                                user_id=9,
                                num_of_sale=0,
                                qty=0,
                                rating=random.randint(0, 5),
                                thumbnail_img=photo_thum_json,
                                photos=phot_list_json,
                                color_id=color_id,
                                characteristics=charr_id,
                                deleted_at=None,
                            )
                            variation.save()
                            var_id = variation.id

                            self.var_translation(var_id, name=var_a)
                            sel = [3, 52, 69]
                            pro_names=[' от Shivaki',' от Tinfis',' от Samsung']
                            for i in range(0, 3):
                                var_a1=var_a+pro_names[i]
                                pro_slug = self.get_slugify(f'{var_a1}')
                                if int(self.slug_unique_for_product(pro_slug)) != 0:
                                    pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                                p=Products(
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
                                    variation_id=var_id,
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
                    element_variation[f'{last_att}'] = sz_list
                    attr_iddd =[]
                    attr_iddd.append(f'{last_att}')
                    # print(f'new_variat={new_variat}\nattr_iddd={attr_iddd}')
                    if len(new_variat)!=0:
                        ddss = list(set(new_variat_attri) | set(attr_iddd))
                        aaaw=self.join_dicts(new_variat,element_variation)
                    else:
                        aaaw=element_variation
                        ddss=attr_iddd
                    Elements.objects.filter(id=elem_id).update(variations=json.dumps(aaaw),variation_attributes=json.dumps(ddss))
            x+=1


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

            name = 'brand'
            if not (os.path.exists(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\{name}.json") and os.path.getsize(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\{name}.json") != 0):
                continue
            bran = self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\{name}.json")
            if bran[-1:] == '.':
                brand = bran.replace('.', '')
            else:
                brand = bran
            if '/' in brand:
                brand = brand.replace('/', '')

            description = mal['Описание']
            json_data = self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\product_characters.json")
            attr_diction_umumiy = {}
            ves = 0
            brand_id = Brands.objects.filter(name=brand)[:1].get().id
            branch_list = []
            for name, values in json_data.items():
                branch_1_dict = {}
                branch1_id = Branches.objects.filter(name=name)[:1].get().id
                branch_1_dict['id'] = branch1_id
                branch_1_dict['title'] = f'{name}'
                res = ast.literal_eval(values)
                atrd_list = []
                for sub_name, sub_value in res.items():
                    attribute_dict = {}
                    charak_list = []
                    if sub_name == 'Вес товара с упаковкой (г)':
                        ves = int(float(sub_value.replace('[', '').replace(']', '').replace(' ', '').replace('г', '').replace("'","")))
                    char_dict = ast.literal_eval(sub_value)
                    # print(f'branch_id=== {branch1_id}----------------attribute name={sub_name}')
                    attri_id = Attributes.objects.filter(Q(name=sub_name) & Q(branch_id=branch1_id))[:1].get().id
                    attribute_dict['id'] = attri_id
                    attribute_dict['attribute'] = f'{sub_name}'
                    char_l = []
                    for char in char_dict:
                        char_name = self.remove_all_spaces(char.lower())
                        # print(f'new  ------{attri_id}--------{char_name}')
                        if ((char_name != '') and (char_name != '-')):
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
                            c_a = {}
                            ggg = str(char_id)
                            c_a['id'] = int(ggg.replace('(),', ''))
                            c_a['name'] = f'{char_name}'
                            char_l.append(c_a)
                            # try:
                            #     attr_chars_id=AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=char_id)[:1].get().id
                            # except ObjectDoesNotExist as den:
                            #     p=AttributeCharacteristic(
                            #         attribute_id=attri_id,
                            #         characteristic_id=char_id
                            #     ).save()
                            #     attr_chars_id=AttributeCharacteristic.objects.filter(attribute_id=attri_id, characteristic_id=char_id)[:1].get().id
                            #
                            #
                            # if aaa =='':
                            #     aaa+=str(attr_chars_id)
                            # elif aaa !='':
                            #     aaa+=','+str(attr_chars_id)
                    attribute_dict['values'] = char_l
                    atrd_list.append(attribute_dict)
                    attr_diction_umumiy[f'{attri_id}'] = charak_list
                branch_1_dict['options'] = atrd_list
                branch_list.append(branch_1_dict)
            oxirgi = {}
            oxirgi['en'] = branch_list
            oxirgi['ru'] = branch_list
            oxirgi['uz'] = branch_list

            app_json = json.dumps(attr_diction_umumiy)

            co = []

            if color != '':
                color_id = Colors.objects.filter(name=f'{color}')[:1].get().id
                co.append(f'{color_id}')
                color_json = json.dumps(co)
            else:
                color_json = None
                color_id = None

            if not Elements.objects.filter(Q(name=a) & Q(category_id=name11) & Q(brand_id=brand_id)).exists():
                if color!='':
                    var_a = a+', '+color
                else:
                    var_a = a
                brand_id=Brands.objects.filter(name=f'{brand}')[:1].get().id
                photo_thum_list=''
                photo_list = ''
                for i in range(1,50):
                    if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{papka}-{i}.jpg'):
                        break
                    else:
                        file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{papka}-{i}.jpg')
                        if not Uploads.objects.filter(file_original_name=f'{papka}-{i}').exists():
                            file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{papka}-{i}.jpg')
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
                elem_slug=self.get_slugify(f'{a}')
                if int(self.slug_unique_for_elem(elem_slug))!=0:
                    elem_slug = elem_slug + f'-{int(self.slug_unique_for_elem(elem_slug))}'

                element_qosh = Elements(
                    name=a,
                    added_by='admin',
                    user_id=9,
                    category_id=int(name11),
                    parent_id=0,
                    brand_id=brand_id,
                    photos=photo_thum_json,
                    thumbnail_img=photo_thum_json,
                    video_provider='youtube',
                    video_link='',
                    tags=int(name22),
                    short_description=json.dumps(oxirgi, ensure_ascii=False),
                    description=description,
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
                    deleted_at=None,
                    on_moderation=0,
                    is_accepted=1,
                    refundable=1,
                )
                element_qosh.save()
                self.elem_translation(element_qosh.id,name=a,des=description)

                var_slug = self.get_slugify(f'{var_a}')
                if int(self.slug_unique_for_var(var_slug)) != 0:
                    var_slug = var_slug + f'-{int(self.slug_unique_for_var(var_slug))}'
                variation = Variations(
                    name=var_a,
                    lowest_price_id=0,
                    slug=var_slug,
                    partnum=papka,
                    element_id=element_qosh.id,
                    prices=random.randint(1,10)*100,
                    short_description=json.dumps(oxirgi, ensure_ascii=False),
                    description=description,
                    variant='',
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

                self.var_translation(variation.id, name=var_a)
                sel = [3, 52, 69]
                pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                for i in range(0, 3):
                    var_a1 = a + pro_names[i]
                    pro_slug = self.get_slugify(f'{var_a1}')
                    if int(self.slug_unique_for_product(pro_slug)) != 0:
                        pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                    Products(
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

                if os.path.isfile(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\sizes.json"):
                    sizes_list=self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\sizes.json")
                    branchh_idd=Branches.objects.filter(name=name)[:1].get().id
                    last_att=Attributes.objects.filter(Q(branch_id=branchh_idd) & Q(name='Размер'))[:1].get().id
                    element_variation={}
                    sz_list=[]
                    for ss in sizes_list[2:]:
                        charr_id=Characteristics.objects.filter(Q(attribute_id=last_att) & Q(name=ss))[:1].get().id
                        sz_list.append(f'{charr_id}')
                        if color != '':
                            var_a = a + ', ' + ss + ', ' + color
                        else:
                            var_a = a + ', ' + ss

                        var_slug = self.get_slugify(f'{var_a}')
                        if int(self.slug_unique_for_var(var_slug)) != 0:
                            var_slug = var_slug + f'-{int(self.slug_unique_for_var(var_slug))}'
                        variation = Variations(
                            name=var_a,
                            lowest_price_id=0,
                            slug=var_slug,
                            partnum=papka,
                            element_id=element_qosh.id,
                            prices=random.randint(1, 10) * 100,
                            short_description=json.dumps(oxirgi, ensure_ascii=False),
                            description=description,
                            variant='',
                            created_at='2021-08-01 16:32:32',
                            updated_at='2021-08-01 16:32:32',
                            user_id=9,
                            num_of_sale=0,
                            qty=0,
                            rating=random.randint(0, 5),
                            thumbnail_img=photo_thum_json,
                            photos=photo_id_json,
                            color_id=color_id,
                            characteristics=charr_id,
                            deleted_at=None,
                        )
                        variation.save()
                        var_id = variation.id
                        self.var_translation(var_id, name=var_a)
                        sel = [3, 52, 69]
                        pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                        for i in range(0, 3):
                            var_a1 = var_a + pro_names[i]
                            pro_slug = self.get_slugify(f'{var_a1}')
                            if int(self.slug_unique_for_product(pro_slug)) != 0:
                                pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                            Products(
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
                                variation_id=var_id,
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
                                element_id=element_qosh.id,
                                sku=None,
                                deleted_at=None,
                                is_quantity_multiplied=0
                            ).save()
                    element_variation[f'{last_att}']=sz_list
                    attr_iddd=[]
                    attr_iddd.append(f'{last_att}')
                    Elements.objects.filter(id=element_qosh.id).update(variations=json.dumps(element_variation),variation_attributes=json.dumps(attr_iddd))
            else:
                elem_id = Elements.objects.filter(Q(name=a) & Q(category_id=name11) & Q(brand_id=brand_id))[:1].get().id
                new_variat =json.loads(Elements.objects.filter(id=elem_id)[:1].get().variations)
                new_variat_attri = json.loads(Elements.objects.filter(id=elem_id)[:1].get().variation_attributes)
                var_json_colors = Elements.objects.filter(id=elem_id)[:1].get().variation_colors
                if var_json_colors != None:
                    variation_colors = json.loads(var_json_colors)
                else:
                    variation_colors = None
                if color != '':
                    color_id = Colors.objects.filter(name=f'{color}')[:1].get().id
                else:
                    color_id = None
                rangi=False
                if color_id != None:
                    if variation_colors == None:
                        variation_colors = list()
                        variation_colors.append(f'{color_id}')
                    elif f'{color_id}' not in variation_colors:
                        variation_colors.append(f'{color_id}')
                        rangi=True
                    variat_json_color1 = json.dumps(variation_colors)
                    variat_json_color = self.remove_space(variat_json_color1)
                    Elements.objects.filter(id=elem_id).update(variation_colors=variat_json_color)

                if not os.path.isfile(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\sizes.json"):
                    if color != '':
                        var_name =f'{a}, {color}'
                    else:
                        var_name=a
                    phot_list=''
                    photo_thum=''
                    if not Variations.objects.filter(name=var_name).exists():
                        for i in range(1, 50):
                            if os.path.isfile(f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{papka}-{i}.jpg'):
                                file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{papka}-{i}.jpg')
                                if not Uploads.objects.filter(file_original_name=f'{papka}-{i}').exists():
                                    file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{papka}-{i}.jpg')
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

                        variation = Variations(
                            name=var_name,
                            lowest_price_id=0,
                            slug=var_slug,
                            partnum=papka,
                            element_id=elem_id,
                            prices=random.randint(1,10)*100,
                            short_description=json.dumps(oxirgi, ensure_ascii=False),
                            description=description,
                            variant='',
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
                        self.var_translation(variation.id, name=var_name)
                        sel = [3, 52, 69]
                        pro_names = [' от Shivaki', ' от Tinfis', ' от Samsung']
                        for i in range(0, 3):
                            var_a1 = var_name + pro_names[i]
                            pro_slug = self.get_slugify(f'{var_a1}')
                            if int(self.slug_unique_for_product(pro_slug)) != 0:
                                pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                            Products(
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
                                variation_id=var_id,
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
                    sizes_list = self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\sizes.json")
                    brann_idd=Branches.objects.filter(name=name)[:1].get().id
                    last_att = Attributes.objects.filter(Q(branch_id=brann_idd) & Q(name='Размер'))[:1].get().id
                    element_variation = {}
                    sz_list = []
                    phot_list = ''
                    photo_thum = ''
                    x = 0
                    for ss in sizes_list:
                        charr_id = Characteristics.objects.filter(Q(attribute_id=last_att) & Q(name=ss))[:1].get().id
                        sz_list.append(f'{charr_id}')
                        if color != '':
                            var_a = a + ', ' + ss + ', ' + color
                        else:
                            var_a = a + ', ' + ss

                        if not Variations.objects.filter(name=var_a).exists():
                            x+=1
                            if x==1:
                                for i in range(1, 50):
                                    if os.path.isfile(f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{papka}-{i}.jpg'):
                                        file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{papka}-{i}.jpg')
                                        if not Uploads.objects.filter(file_original_name=f'{papka}-{i}').exists():
                                            file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{papka}-{i}.jpg')
                                            b_name1='variation'
                                            photos_id = self.uploads(f'{papka}-{i}', file_name, file_size,b_name1)
                                        else:
                                            photos_id=Uploads.objects.filter(file_original_name=f'{papka}-{i}')[:1].get().id

                                        if i == 1:
                                            photo_thum += f'{photos_id}'
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
                                            if i == 2:
                                                phot_list += f'{photos_id}'
                                            else:
                                                phot_list += f',{photos_id}'
                                    else:
                                        break
                                phot_list_json = phot_list
                                photo_thum_json = photo_thum

                            var_slug = self.get_slugify(f'{var_a}')
                            if int(self.slug_unique_for_var(var_slug)) != 0:
                                var_slug = var_slug + f'-{int(self.slug_unique_for_var(var_slug))}'
                            variation = Variations(
                                name=var_a,
                                lowest_price_id=0,
                                slug=var_slug,
                                partnum=papka,
                                element_id=elem_id,
                                prices=random.randint(1, 10) * 100,
                                short_description=json.dumps(oxirgi, ensure_ascii=False),
                                description=description,
                                variant='',
                                created_at='2021-08-01 16:32:32',
                                updated_at='2021-08-01 16:32:32',
                                user_id=9,
                                num_of_sale=0,
                                qty=0,
                                rating=random.randint(0, 5),
                                thumbnail_img=photo_thum_json,
                                photos=phot_list_json,
                                color_id=color_id,
                                characteristics=charr_id,
                                deleted_at=None,
                            )
                            variation.save()
                            var_id = variation.id

                            self.var_translation(var_id, name=var_a)
                            sel = [3, 52, 69]
                            pro_names=[' от Shivaki',' от Tinfis',' от Samsung']
                            for i in range(0, 3):
                                var_a1=var_a+pro_names[i]
                                pro_slug = self.get_slugify(f'{var_a1}')
                                if int(self.slug_unique_for_product(pro_slug)) != 0:
                                    pro_slug = pro_slug + f'-{int(self.slug_unique_for_product(pro_slug))}'
                                Products(
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
                                    variation_id=var_id,
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
                    element_variation[f'{last_att}'] = sz_list
                    attr_iddd =[]
                    attr_iddd.append(f'{last_att}')
                    # print(f'new_variat={new_variat}\nattr_iddd={attr_iddd}')
                    if len(new_variat)!=0:
                        ddss = list(set(new_variat_attri) | set(attr_iddd))
                        aaaw=self.join_dicts(new_variat,element_variation)
                    else:
                        aaaw=element_variation
                        ddss=attr_iddd
                    Elements.objects.filter(id=elem_id).update(variations=json.dumps(aaaw),variation_attributes=json.dumps(ddss))
            x+=1
    
    def attribute_new_var(self):
        charakters=Elements.objects.filter(~Q(variations='[]')).all()
        for a in charakters:
            new=self.join_dicts(json.loads(a.characteristics),json.loads(a.variations))
            char_neww={}
            for b in json.loads(a.variations).keys():
                char_neww[f'{b}']=new[f'{b}']
            Elements.objects.filter(id=a.id).update(characteristics=json.dumps(new),variations=json.dumps(char_neww))



    def join_dicts(self,d1, d2):
        k1 = []
        k2 = []
        for k in d1.keys():
            k1.append(k)
        for k in d2.keys():
            k2.append(k)
        for k in k1:
            if k not in k2:
                list_d1 = d1[f'{k}']
                d2[f'{k}'] = list_d1
            else:
                a = d1[f'{k}']
                b = d2[f'{k}']
                resultList = list(set(a) | set(b))
                d2[f'{k}'] = resultList
        return d2






class Command(BaseCommand):
    help='Parsing Wildberries'
    def handle(self, *args, **options):
        p=Parse_All()
        # p.get_category_and_link()
        p.attribute_new_var()
        # p.get_dict_d(1,2)
        # p.get_dict(1,2)
        # p.element(cate_name={'Планшеты': 'https://www.wildberries.ru/catalog/elektronika/planshety'},number=2)
 #



 # p.put_branch(cate_name={'Планшеты': 'https://www.wildberries.ru/catalog/elektronika/planshety'},number=2)






