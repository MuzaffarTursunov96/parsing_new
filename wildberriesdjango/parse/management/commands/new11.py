import time
from collections import namedtuple
from bs4 import  BeautifulSoup
import  requests
import os
import ast
from slugify import slugify
import shutil
import json
from parse.models import AttributeCategory,AttributeCharacteristic,AttributeTranslations,Attributes,BranchTranslations,Branches,BrandTranslations,Brands,Categories,CategoryTranslations,CharacteristicTranslations,Characteristics,ColorTranslations,Colors,ElementTranslations,Elements,Products,Uploads,VariationTranslations,Variations,BrandCategory
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
    def check_exists_d(self, name1,name2,papka):
        absolute_path = os.path.abspath(__file__)
        filees = os.path.isfile(f'{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\product_detail.html')
        return filees

    def get_category_and_link(self):
        absolute_path = os.path.abspath(__file__)
        category_0_list = []
        category_1_list = []
        category_2_list = []
        category_2_dict_link=[]
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
        for cate_2 in category_2_list:
            try:
                cate_22 = Categories.objects.filter(parent_id=cate_2)
                if os.path.isdir(f"{os.path.dirname(absolute_path)}\{cate_22}"):
                    self.cate_dir(cate_22)
                for cate_222 in cate_22:
                    self.get_dict_3(cate_2,cate_222.id, cate_222.link)
            except ObjectDoesNotExist as ex:
                cate_22=cate_2.id
                cate_22_link=cate_2.link
                if cate_22_link !='':
                    self.get_dict(cate_22,cate_22_link)






    def category(self, category_name, papka, name='Планшеты на Android'):
        absolute_path = os.path.abspath(__file__)
        with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\category.json", 'w',
                  encoding='utf-8') as file:
            json.dump(name, file, indent=4, ensure_ascii=False)

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

    def get_dict(self, name,link):
        absolute_path = os.path.abspath(__file__)
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name}'):
            self.cate_dir(name)
        for i in range(1,2):
            if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{name}\{i}.html'):
                response = self.get_html(f'{link}')
                time.sleep(3)
                source = response.text
                with open(f"{os.path.dirname(absolute_path)}\{name}\{i}.html", 'w', encoding='utf-8') as file:
                    file.write(source)

    def get_dict_3(self, name_c,name_d,link):
        absolute_path = os.path.abspath(__file__)
        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name_c}\{name_d}'):
            self.cate_dir_d(name_c,name_d)
        for i in range(1,2):
            if not os.path.isfile(f'{os.path.dirname(absolute_path)}\{name_c}\{name_d}\{i}.html'):
                response = self.get_html(f'{link}')
                time.sleep(3)
                source = response.text
                with open(f"{os.path.dirname(absolute_path)}\{name_c}\{name_d}\{i}.html", 'w', encoding='utf-8') as file:
                    file.write(source)

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
    def check_img_dir_d(self, name1,name2, papka, images):
        absolute_path = os.path.abspath(__file__)
        if os.path.isdir(f'{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\{images}'):
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

    def get_path_c(self):
        absolute_path = os.path.abspath(__file__)
        category_2_list=[]
        for cate_2 in Categories.objects.filter(level=2):
            if cate_2.link !='':
                category_2_list.append(cate_2.id)
        for cate_22 in category_2_list:
            try:
                d_category =Categories.objects.filter(parent_id=cate_22)
                for cate_222 in d_category:
                    for i in range(1, 2):
                        with open(f"{os.path.dirname(absolute_path)}\{cate_22}\{cate_222.id}\{i}.html", encoding='utf-8') as file:
                            source = file.read()
                        self.product_css_d(source,cate_22, cate_222.id)
                        self.product_characters_dc(source,cate_22,cate_222.id)
                        self.put_attributes_d(source,cate_22,cate_222.id)
            except ObjectDoesNotExist as ex:
                for i in range(1, 2):
                    with open(f"{os.path.dirname(absolute_path)}\{cate_22}\{i}.html", encoding='utf-8') as file:
                        source = file.read()
                    self.product_css_c(source,cate_22)
                    self.product_characters_cc(source,cate_22)
                    self.put_attributes_c(source,cate_22)



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

    def product_css_c(self, source, name):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        for product_hrefs in all_product:
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
                product_brand_name = self.replace_drop(product_brand_name1)

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
                        image = prod_image.find('img').get('src')
                        req_img = self.test_request(f'https:{str(image[0:22])}big{str(image[24:])}').content
                        with open(
                                f"{os.path.dirname(absolute_path)}\{name}\{papka}\images\{papka}-{count_img}.jpg",
                                'wb') as file:
                            file.write(req_img)
                        count_img += 1

    def product_css_d(self, source, name1,name2):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            print(papka)
            absolute_path = os.path.abspath(__file__)
            if self.prod_papka_yaratish_c(name1,name2, papka):
                parent_dir = f'{os.path.dirname(absolute_path)}\{name1}\{name2}'
                path = os.path.join(parent_dir, f'{papka}')
                os.mkdir(path)
                par_img = f'{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}'
                if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\images'):
                    path_img = os.path.join(par_img, 'images')
                    os.mkdir(path_img)
            if self.check_exists_d(name1,name2, papka):
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

            if self.check_img_dir_d(name1,name2, papka, 'images'):
                prod_images = source.find(class_='same-part-kt').find(class_='swiper-wrapper').find_all('li')
                count_img = 1
                for prod_image in prod_images:
                    if 'slide--video' in prod_image['class']:
                        continue
                    else:
                        image = prod_image.find('img').get('src')
                        req_img = self.test_request(f'https:{str(image[0:22])}big{str(image[24:])}').content
                        with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\images\{papka}-{count_img}.jpg",'wb') as file:
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
                table_name = source.find(class_='same-part-kt__show-sizes').get_text()
                size_list = []
                for size in source.find(class_='same-part-kt__sizes-list').find_all(class_='sizes-list__item'):
                    if size.find('label').find(class_='sizes-list__size-ru')!=None:
                        size_val = size.find('label').find(class_='sizes-list__size-ru').get_text()
                    elif size.find('label').find(class_='sizes-list__size')!=None:
                        size_val = size.find('label').find(class_='sizes-list__size').get_text()
                    size_list.append(f'{size_val}')
                    ssa = {}
                    ssa['Размер'] = list(f'{size_list[0]}')
                cap_dict[f'{caption_name}'] = f'{ssa}'
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\sizes.json", 'w',
                          encoding='utf-8') as file:
                    json.dump(size_list, file, indent=4, ensure_ascii=False)

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\description.json", 'w',
                      encoding='utf-8') as file:
                json.dump(descrip, file, indent=4, ensure_ascii=False)

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{papka}\product_characters.json", 'w',
                      encoding='utf-8') as file:
                json.dump(cap_dict, file, indent=4, ensure_ascii=False)


    def product_characters_dc(self, source, name1,name2):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            try:
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\product_detail.html",
                          encoding='utf-8') as file:
                    soup = file.read()
            except FileNotFoundError as ex:
                continue
            # print(papka)
            source = BeautifulSoup(soup, 'lxml')
            try:
                caption = source.find(class_='product-params').find(class_='product-params__table').find('caption')
            except AttributeError as ex:
                pass


            print(papka)
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
                table_name = source.find(class_='same-part-kt__show-sizes').get_text()
                size_list = []
                for size in source.find(class_='same-part-kt__sizes-list').find_all(class_='sizes-list__item'):
                    if size.find('label').find(class_='sizes-list__size-ru')!=None:
                        size_val = size.find('label').find(class_='sizes-list__size-ru').get_text()
                    elif size.find('label').find(class_='sizes-list__size')!=None:
                        size_val = size.find('label').find(class_='sizes-list__size').get_text()

                    size_list.append(f'{size_val}')
                    ssa={}
                    ssa['Размер']=list(f'{size_list[0]}')
                cap_dict[f'{caption_name}']=f'{ssa}'
                with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\sizes.json", 'w',
                          encoding='utf-8') as file:
                    json.dump(size_list, file, indent=4, ensure_ascii=False)


            with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\description.json", 'w',
                      encoding='utf-8') as file:
                json.dump(descrip, file, indent=4, ensure_ascii=False)

            with open(f"{os.path.dirname(absolute_path)}\{name1}\{name2}\{papka}\product_characters.json", 'w',
                      encoding='utf-8') as file:
                json.dump(cap_dict, file, indent=4, ensure_ascii=False)







    def get_slugify(self,name):
        return slugify(f'{name}', to_lower=True)




    #######################        Baza       #############################


    def get_attributes(self,name):
        atbute_id = AttributeTranslations.objects.filter(name__ru=f"{name}")[:1].get().id
        attribute_id = Attributes.objects.filter(name=atbute_id)[:1].get().id
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

    def attr_charakteristic(self,attr_id,char_id):
        p=AttributeCharacteristic(
            attribute_id=attr_id,
            characteristic_id=char_id
        ).save()


    def put_attributes_c(self,name1):
        absolute_path = os.path.abspath(__file__)
        for i in range(1,2):
            print(f'{i} chi papka harakteristika')
            with open(f"{os.path.dirname(absolute_path)}\\{name1}\\{i}.html", encoding='utf-8') as file:
                source = file.read()
            self.product_attributes_c(source, name1)

    def product_attributes_c(self, source,name11):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)

        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            try:
                json_data=self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\product_characters.json")
            except FileNotFoundError as ex:
                continue

            for name, values in json_data.items():
                if not BranchTranslations.objects.filter(name__ru=f"{name}").exists():
                    bran_tr = {'uz': f'{name}', 'ru': f'{name}', 'en': f'{name}', 'default': f'{name}'}
                    bb = BranchTranslations.objects.create(
                        name=bran_tr,
                        created_at='2021-05-21 02:19:37',
                        updated_at='2021-05-21 02:19:37',
                        deleted_at=None)
                    bb.save()
                    bro = Branches.objects.create(
                        name=bb.id,
                        created_at='2021-07-01 17:44:48',
                        updated_at='2021-07-01 17:44:48',
                    )
                    bro.save()
                    bro1 = bro.id
                else:
                    bb = BranchTranslations.objects.filter(name__ru=f"{name}")[:1].get().id
                    bro1 = Branches.objects.filter(name=bb)[:1].get().id

                res = ast.literal_eval(values)
                for sub_name, sub_value in res.items():
                    if not AttributeTranslations.objects.filter(name__ru=f"{sub_name}").exists():
                        aa_t = {'uz': f'{sub_name}', 'ru': f'{sub_name}', 'en': f'{sub_name}', 'default': f'{sub_name}'}
                        aaa_t = AttributeTranslations.objects.create(
                            name=aa_t,
                            created_at='2021-05-21 02:19:37',
                            updated_at='2021-05-21 02:19:37', deleted_at=None)
                        aaa_t.save()
                        aa_tt = Attributes(
                            branch_id=bro1,
                            name=aaa_t.id,
                            combination=0,
                            created_at='2021-05-20 20:14:08',
                            updated_at='2021-05-20 20:14:08',
                            deleted_at=None
                        )
                        aa_tt.save()
                        self.put_category_and_attr(name11, aa_tt.id)
                    else:
                        tttt = AttributeTranslations.objects.filter(name__ru=f"{sub_name}")[:1].get().id
                        if Attributes.objects.filter(Q(name=tttt) & Q(branch_id=bro1)).exists():
                            attr_id = Attributes.objects.filter(Q(name=tttt) & Q(branch_id=bro1))[:1].get().id
                        else:
                            aa_tt = Attributes(
                                branch_id=bro1,
                                name=tttt,
                                combination=0,
                                created_at='2021-05-20 20:14:08',
                                updated_at='2021-05-20 20:14:08',
                                deleted_at=None
                            )
                            aa_tt.save()
                            attr_id = aa_tt.id
                        self.put_category_and_attr(name11, attr_id)

                #######################
                for sub_name, sub_value in res.items():
                    x = ast.literal_eval(sub_value)
                    attribute_id = self.get_attributes(f'{sub_name}')
                    for char_val in range(0, len(x)):
                        cha_rem = self.remove_all_spaces(x[char_val].lower())
                        slug = self.get_slugify(f'{cha_rem}')
                        if self.slug_unique_for_chars(slug) != 0:
                            slug = slug + f'-{int(self.slug_unique_for_chars(slug)) + 1}'

                        if not CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}").exists():
                            char_x = {'uz': f'{cha_rem}', 'ru': f'{cha_rem}', 'en': f'{cha_rem}',
                                      'default': f'{cha_rem}'}

                            chaa = CharacteristicTranslations.objects.create(
                                name=char_x,
                                created_at='2021-05-20 20:14:08',
                                updated_at='2021-05-20 20:14:08',
                                deleted_at=None
                            )
                            chaa.save()
                            p = Characteristics(
                                attribute_id=attribute_id,
                                name=chaa.id,
                                slug=slug,
                                created_at='2021-05-29 00:55:49',
                                updated_at='2021-05-20 21:05:09',
                                deleted_at=None,
                            ).save()
                        elif not Characteristics.objects.filter(Q(attribute_id=attribute_id) & Q(name=CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}")[:1].get().id)).exists():
                            p = Characteristics(
                                attribute_id=attribute_id,
                                name=CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}")[:1].get().id,
                                slug=slug,
                                created_at='2021-05-29 00:55:49',
                                updated_at='2021-05-20 21:05:09',
                                deleted_at=None,
                            ).save()
                    if os.path.isfile(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\sizes.json"):
                        xx = self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\sizes.json")
                        for char_val in range(0, len(xx)):
                            cha_rem = self.remove_all_spaces(xx[char_val].lower())
                            slug = self.get_slugify(f'{cha_rem}')
                            if self.slug_unique_for_chars(slug) != 0:
                                slug = slug + f'-{int(self.slug_unique_for_chars(slug)) + 1}'

                            if not CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}").exists():
                                char_x = {'uz': f'{cha_rem}', 'ru': f'{cha_rem}', 'en': f'{cha_rem}',
                                          'default': f'{cha_rem}'}

                                chaa = CharacteristicTranslations.objects.create(
                                    name=char_x,
                                    created_at='2021-05-20 20:14:08',
                                    updated_at='2021-05-20 20:14:08',
                                    deleted_at=None
                                )
                                chaa.save()
                                p = Characteristics(
                                    attribute_id=attribute_id,
                                    name=chaa.id,
                                    slug=slug,
                                    created_at='2021-05-29 00:55:49',
                                    updated_at='2021-05-20 21:05:09',
                                    deleted_at=None,
                                ).save()
                            elif not Characteristics.objects.filter(Q(attribute_id=attribute_id) & Q(
                                    name=CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}")[
                                         :1].get().id)).exists():
                                p = Characteristics(
                                    attribute_id=attribute_id,
                                    name=CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}")[:1].get().id,
                                    slug=slug,
                                    created_at='2021-05-29 00:55:49',
                                    updated_at='2021-05-20 21:05:09',
                                    deleted_at=None,
                                ).save()

            brand_n = 'brand'
            a=self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\{brand_n}.json")
            if a[-1:] == '.':
                product_brand_nam = a.replace('.', '')
            else:
                product_brand_nam = a

            if '/' in product_brand_nam:
                b_name = product_brand_nam.replace('/', '')
            else:
                b_name = product_brand_nam

            file_size = os.path.getsize(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{b_name}.jpg")
            if not Uploads.objects.filter(file_original_name=b_name).exists():
                file_name = self.hash_and_move(b_name,f"{os.path.dirname(absolute_path)}\{name11}\{papka}\images\{b_name}.jpg")
                brand_id = self.uploads(b_name, file_name, file_size)

            slug = self.get_slugify(f'{b_name}')
            if self.slug_unique_for_brand(slug) != 0:
                slug = slug + f'-{int(self.slug_unique_for_brand(slug)) + 1}'
            if not BrandTranslations.objects.filter(name__ru=f"{b_name}").exists():
                br_jj = {'uz': f'{b_name}', 'ru': f'{b_name}', 'en': f'{b_name}', 'default': f'{b_name}'}
                brr = BrandTranslations.objects.create(
                    name=br_jj,
                    created_at='2021-05-21 02:19:37',
                    updated_at='2021-05-21 02:19:37',
                    deleted_at=None
                )
                brr.save()
                brad_id = Uploads.objects.filter(file_original_name=f'{b_name}')[:1].get().id
                Brands(
                    name=brr.id,
                    logo=brad_id,
                    top=0,
                    slug=slug,
                    meta_title=f'{b_name} в онлайн гипермаркете TINFIS',
                    meta_description=f'Огромный выбор продукции бренда "{b_name}" в нашем онлайн гипермаркете.  100% гарантия качества от лучших магазинов!',
                    created_at='2021-05-21 02:19:37',
                    updated_at='2021-05-21 02:19:37'
                ).save()

            color = self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{papka}\description.json")[
                'color']
            if not ColorTranslations.objects.filter(name__ru=f"{color}").exists():
                if color != '':
                    col_tr = {'uz': f'{color}', 'ru': f'{color}', 'en': f'{color}', 'default': f'{color}'}
                    ccc = ColorTranslations.objects.create(
                        name=col_tr,
                        created_at='2018-11-04 19:12:26',
                        updated_at='2018-11-04 19:12:26',
                        deleted_at=None
                    )
                    ccc.save()
                    p = Colors(
                        name=ccc.id,
                        code='#CD5C5C',
                        created_at='2018-11-04 19:12:26',
                        updated_at='2018-11-04 19:12:26'
                    ).save()

    def put_attributes_d(self,name1,name2):
        absolute_path = os.path.abspath(__file__)
        for i in range(1,2):
            print(f'{i} chi papka harakteristika')
            with open(f"{os.path.dirname(absolute_path)}\\{name1}\\{name2}\\{i}.html", encoding='utf-8') as file:
                source = file.read()
            self.product_attributes_c(source, name1,name2)

    def product_attributes_d(self, source,name11,name22):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)

        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            try:
                json_data=self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\product_characters.json")
            except FileNotFoundError as ex:
                continue

            for name, values in json_data.items():
                if not BranchTranslations.objects.filter(name__ru=f"{name}").exists():
                    bran_tr = {'uz': f'{name}', 'ru': f'{name}', 'en': f'{name}', 'default': f'{name}'}
                    bb = BranchTranslations.objects.create(
                        name=bran_tr,
                        created_at='2021-05-21 02:19:37',
                        updated_at='2021-05-21 02:19:37',
                        deleted_at=None)
                    bb.save()
                    bro = Branches.objects.create(
                        name=bb.id,
                        created_at='2021-07-01 17:44:48',
                        updated_at='2021-07-01 17:44:48',
                    )
                    bro.save()
                    bro1 = bro.id
                else:
                    bb = BranchTranslations.objects.filter(name__ru=f"{name}")[:1].get().id
                    bro1 = Branches.objects.filter(name=bb)[:1].get().id

                res = ast.literal_eval(values)
                for sub_name, sub_value in res.items():
                    if not AttributeTranslations.objects.filter(name__ru=f"{sub_name}").exists():
                        aa_t = {'uz': f'{sub_name}', 'ru': f'{sub_name}', 'en': f'{sub_name}', 'default': f'{sub_name}'}
                        aaa_t = AttributeTranslations.objects.create(
                            name=aa_t,
                            created_at='2021-05-21 02:19:37',
                            updated_at='2021-05-21 02:19:37', deleted_at=None)
                        aaa_t.save()
                        aa_tt = Attributes(
                            branch_id=bro1,
                            name=aaa_t.id,
                            combination=0,
                            created_at='2021-05-20 20:14:08',
                            updated_at='2021-05-20 20:14:08',
                            deleted_at=None
                        )
                        aa_tt.save()
                        self.put_category_and_attr(name11, aa_tt.id)
                    else:
                        tttt = AttributeTranslations.objects.filter(name__ru=f"{sub_name}")[:1].get().id
                        if Attributes.objects.filter(Q(name=tttt) & Q(branch_id=bro1)).exists():
                            attr_id = Attributes.objects.filter(Q(name=tttt) & Q(branch_id=bro1))[:1].get().id
                        else:
                            aa_tt = Attributes(
                                branch_id=bro1,
                                name=tttt,
                                combination=0,
                                created_at='2021-05-20 20:14:08',
                                updated_at='2021-05-20 20:14:08',
                                deleted_at=None
                            )
                            aa_tt.save()
                            attr_id = aa_tt.id
                        self.put_category_and_attr(name11, attr_id)

                #######################
                for sub_name, sub_value in res.items():
                    x = ast.literal_eval(sub_value)
                    attribute_id = self.get_attributes(f'{sub_name}')
                    for char_val in range(0, len(x)):
                        cha_rem = self.remove_all_spaces(x[char_val].lower())
                        slug = self.get_slugify(f'{cha_rem}')
                        if self.slug_unique_for_chars(slug) != 0:
                            slug = slug + f'-{int(self.slug_unique_for_chars(slug)) + 1}'

                        if not CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}").exists():
                            char_x = {'uz': f'{cha_rem}', 'ru': f'{cha_rem}', 'en': f'{cha_rem}',
                                      'default': f'{cha_rem}'}

                            chaa = CharacteristicTranslations.objects.create(
                                name=char_x,
                                created_at='2021-05-20 20:14:08',
                                updated_at='2021-05-20 20:14:08',
                                deleted_at=None
                            )
                            chaa.save()
                            p = Characteristics(
                                attribute_id=attribute_id,
                                name=chaa.id,
                                slug=slug,
                                created_at='2021-05-29 00:55:49',
                                updated_at='2021-05-20 21:05:09',
                                deleted_at=None,
                            ).save()
                        elif not Characteristics.objects.filter(Q(attribute_id=attribute_id) & Q(name=CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}")[:1].get().id)).exists():
                            p = Characteristics(
                                attribute_id=attribute_id,
                                name=CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}")[:1].get().id,
                                slug=slug,
                                created_at='2021-05-29 00:55:49',
                                updated_at='2021-05-20 21:05:09',
                                deleted_at=None,
                            ).save()
                    if os.path.isfile(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\sizes.json"):
                        xx=self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\sizes.json")
                        for char_val in range(0, len(xx)):
                            cha_rem = self.remove_all_spaces(xx[char_val].lower())
                            slug = self.get_slugify(f'{cha_rem}')
                            if self.slug_unique_for_chars(slug) != 0:
                                slug = slug + f'-{int(self.slug_unique_for_chars(slug)) + 1}'

                            if not CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}").exists():
                                char_x = {'uz': f'{cha_rem}', 'ru': f'{cha_rem}', 'en': f'{cha_rem}',
                                          'default': f'{cha_rem}'}

                                chaa = CharacteristicTranslations.objects.create(
                                    name=char_x,
                                    created_at='2021-05-20 20:14:08',
                                    updated_at='2021-05-20 20:14:08',
                                    deleted_at=None
                                )
                                chaa.save()
                                p = Characteristics(
                                    attribute_id=attribute_id,
                                    name=chaa.id,
                                    slug=slug,
                                    created_at='2021-05-29 00:55:49',
                                    updated_at='2021-05-20 21:05:09',
                                    deleted_at=None,
                                ).save()
                            elif not Characteristics.objects.filter(Q(attribute_id=attribute_id) & Q(name=CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}")[:1].get().id)).exists():
                                p = Characteristics(
                                    attribute_id=attribute_id,
                                    name=CharacteristicTranslations.objects.filter(name__ru=f"{cha_rem}")[:1].get().id,
                                    slug=slug,
                                    created_at='2021-05-29 00:55:49',
                                    updated_at='2021-05-20 21:05:09',
                                    deleted_at=None,
                                ).save()

            brand_n = 'brand'
            a=self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\{brand_n}.json")
            if a[-1:] == '.':
                product_brand_nam = a.replace('.', '')
            else:
                product_brand_nam = a

            if '/' in product_brand_nam:
                b_name = product_brand_nam.replace('/', '')
            else:
                b_name = product_brand_nam

            file_size = os.path.getsize(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{b_name}.jpg")
            if not Uploads.objects.filter(file_original_name=b_name).exists():
                file_name = self.hash_and_move(b_name,f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\images\{b_name}.jpg")
                brand_id = self.uploads(b_name, file_name, file_size)

            slug = self.get_slugify(f'{b_name}')
            if self.slug_unique_for_brand(slug) != 0:
                slug = slug + f'-{int(self.slug_unique_for_brand(slug)) + 1}'
            if not BrandTranslations.objects.filter(name__ru=f"{b_name}").exists():
                br_jj = {'uz': f'{b_name}', 'ru': f'{b_name}', 'en': f'{b_name}', 'default': f'{b_name}'}
                brr = BrandTranslations.objects.create(
                    name=br_jj,
                    created_at='2021-05-21 02:19:37',
                    updated_at='2021-05-21 02:19:37',
                    deleted_at=None
                )
                brr.save()
                brad_id = Uploads.objects.filter(file_original_name=f'{b_name}')[:1].get().id
                Brands(
                    name=brr.id,
                    logo=brad_id,
                    top=0,
                    slug=slug,
                    meta_title=f'{b_name} в онлайн гипермаркете TINFIS',
                    meta_description=f'Огромный выбор продукции бренда "{b_name}" в нашем онлайн гипермаркете.  100% гарантия качества от лучших магазинов!',
                    created_at='2021-05-21 02:19:37',
                    updated_at='2021-05-21 02:19:37'
                ).save()

            color = self.read_json(f"{os.path.dirname(absolute_path)}\{name11}\{name22}\{papka}\description.json")['color']
            if not ColorTranslations.objects.filter(name__ru=f"{color}").exists():
                if color != '':
                    col_tr = {'uz': f'{color}', 'ru': f'{color}', 'en': f'{color}', 'default': f'{color}'}
                    ccc = ColorTranslations.objects.create(
                        name=col_tr,
                        created_at='2018-11-04 19:12:26',
                        updated_at='2018-11-04 19:12:26',
                        deleted_at=None
                    )
                    ccc.save()
                    p = Colors(
                        name=ccc.id,
                        code='#CD5C5C',
                        created_at='2018-11-04 19:12:26',
                        updated_at='2018-11-04 19:12:26'
                    ).save()


    def read_file(self,path):
        file = open(path, "r",encoding='utf-8')
        data = file.read()
        file.close()
        return data


    def uploads(self,name,file_name,file_size):
        n='all'
        p = Uploads(
            file_original_name=name,
            file_name=f'uploads\{n}\{file_name}.jpg',
            user_id=9,
            file_size=file_size,
            extension='jpg',
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

    def remove_all_spaces(self,str):
        return "".join(str.strip())

    def put_category_and_attr(self, cate_id, atr_id):
        if not AttributeCategory.objects.filter(Q(attribute_id=f'{atr_id}') & Q(category_id=int(cate_id))).exists():
            p = AttributeCategory(
                attribute_id=atr_id,
                category_id=int(cate_id)
            ).save()

    def slug_unique_for_var(self, slug):
        if Variations.objects.filter(slug__startswith=slug).exists():
            a = Variations.objects.filter(slug__startswith=slug).count()
            return a
        else:
            return 0

    def slug_unique_for_chars(self, slug):
        if Characteristics.objects.filter(slug__startswith=slug).exists():
            a = Characteristics.objects.filter(slug__startswith=slug).count()
            return a
        else:
            return 0

    def slug_unique_for_elem(self, slug):
        if Elements.objects.filter(slug__startswith=slug).exists():
            a = Elements.objects.filter(slug__startswith=slug).count()
            return a
        else:
            return 0

    def slug_unique_for_brand(self, slug):
        if Brands.objects.filter(slug__startswith=slug).exists():
            a = Brands.objects.filter(slug__startswith=slug).count()
            return a
        else:
            return 0

    def element_c(self, nam11):
        absolute_path = os.path.abspath(__file__)
        for i in range(1 , 2):
            print(f'{i} chi sahifa #########################')
            with open(f"{os.path.dirname(absolute_path)}\{nam11}\{i}.html", encoding='utf-8') as file:
                source = file.read()
            self.put_elements(source, nam11)

    def put_elements_c(self, source, nam111):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        absolute_path = os.path.abspath(__file__)

        if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{nam111}\images'):
            parent_dir = f'{os.path.dirname(absolute_path)}\{nam111}'
            path = os.path.join(parent_dir, f'images')
            os.mkdir(path)

        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            if not os.path.isdir(f"{os.path.dirname(absolute_path)}\{nam111}\{papka}"):
                continue
            ann=self.remove_all_spaces(product_hrefs.find(class_='goods-name').getText())
            ann1=ann
            name = 'brand'
            if not (os.path.exists(f"{os.path.dirname(absolute_path)}\{nam111}\{papka}\{name}.json") and os.path.getsize(f"{os.path.dirname(absolute_path)}\{nam111}\{papka}\{name}.json") != 0):
                continue
            br1 = self.read_json(f"{os.path.dirname(absolute_path)}\{nam111}\{papka}\{name}.json")
            bran = br1  # json.loads(br1)
            if bran[-1:] == '.':
                brand = bran.replace('.', '')
            else:
                brand = bran
            if '/' in brand:
                brand = brand.replace('/', '')

            tag_id = ''
            bbb_t = BrandTranslations.objects.filter(name__ru=f"{brand}")[:1].get().id
            brand_id = Brands.objects.filter(name=bbb_t)[:1].get().id
            if not BrandCategory.objects.filter(Q(brand_id=brand_id) & Q(category_id=nam111)).exists():
                BrandCategory(
                    brand_id=brand_id,
                    category_id=nam111
                ).save()
            mal = self.read_json(f"{os.path.dirname(absolute_path)}\{nam111}\{papka}\description.json")
            color = mal['color']
            description = mal['Описание']
            ######Character###########
            json_data = self.read_json(f"{os.path.dirname(absolute_path)}\{nam111}\{papka}\product_characters.json")
            attr_diction_umumiy = {}
            ves = 0
            branch_list = []
            single_branch_name=''
            for name, values in json_data.items():
                single_branch_name=name
                branch_1_dict = {}
                branch_1_t = BranchTranslations.objects.filter(name__ru=f"{name}")[:1].get().id
                branch1_id = Branches.objects.filter(name=branch_1_t)[:1].get().id
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
                    attrr_tt = AttributeTranslations.objects.filter(name__ru=f"{sub_name}")[:1].get().id
                    attri_id = Attributes.objects.filter(Q(name=attrr_tt)&Q(branch_id=branch1_id))[:1].get().id
                    attribute_dict['id'] = attri_id
                    attribute_dict['attribute'] = f'{sub_name}'
                    char_l = []
                    for char in char_dict:
                        char_name = self.remove_all_spaces(char.lower())
                        chaa_ttt = CharacteristicTranslations.objects.filter(name__ru=f"{char_name}")[:1].get().id
                        char_id = Characteristics.objects.filter(Q(name=chaa_ttt) & Q(attribute_id=attri_id))[:1].get().id
                        charak_list.append(f'{char_id}')
                        c_a = {}
                        ggg = str(char_id)
                        c_a['id'] = int(ggg.replace('(),', ''))
                        c_a['name'] = f'{char_name}'
                        char_l.append(c_a)
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
            ############end--Charakter###########
            if not ElementTranslations.objects.filter(name__ru=f"{ann}").exists():
                try:
                    sz=self.read_json(f"{os.path.dirname(absolute_path)}\{nam111}\{papka}\sizes.json")
                    if color != '':
                        var_a = ann + ', ' + sz[0] + ', ' + color
                    else:
                        var_a = ann + ', ' + sz[0]
                except FileNotFoundError as ex:
                    if color != '':
                        var_a = ann +', ' + color
                    else:
                        var_a = ann

                co = []
                if color != '':
                    colll = ColorTranslations.objects.filter(name__ru=f"{color}")[:1].get().id
                    color_id = Colors.objects.filter(name=colll)[:1].get().id
                    co.append(f'{color_id}')
                    color_json = json.dumps(co)
                else:
                    color_json = None
                    color_id = None
                var_js = ''
                photo_thum_list = ''
                photo_list = ''
                for i in range(1, 50):
                    if not os.path.isfile(
                            f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\images\{papka}-{i}.jpg'):
                        break
                    else:
                        file_name = self.hash_and_move(f'{papka}-{i}',f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\images\{papka}-{i}.jpg')
                        file_size = os.path.getsize(f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\images\{papka}-{i}.jpg')
                        n = 'all'
                        photos_id = self.uploads(f'{papka}-{i}', file_name, file_size)
                        if i == 1:
                            photo_thum_list += f'{photos_id}'
                        else:
                            if i == 2:
                                photo_list += f'{photos_id}'
                            else:
                                photo_list += f',{photos_id}'
                photo_id_json = photo_list
                photo_thum_json = photo_thum_list
                elem_slug = self.get_slugify(f'{ann}')
                if int(self.slug_unique_for_elem(elem_slug)) != 0:
                    elem_slug = elem_slug + f'-{int(self.slug_unique_for_elem(elem_slug))}'
                elem_a = {'uz': f'{ann}', 'ru': f'{ann}', 'en': f'{ann}', 'default': f'{ann}', 'meta_title': f'{ann}'}
                elem_desc = {'uz': f'{description}', 'ru': f'{description}', 'en': f'{description}'}
                n = ElementTranslations.objects.create(name=elem_a, description=elem_desc,created_at='2021-05-21 02:19:37',updated_at='2021-05-21 02:19:37', deleted_at=None)
                n.save()
                element_qosh = Elements(
                    name=n.id,
                    added_by='admin',
                    user_id=9,
                    category_id=int(nam111),
                    parent_id=0,
                    brand_id=brand_id,
                    photos=photo_id_json,
                    thumbnail_img=photo_thum_json,
                    video_provider='youtube',
                    video_link='',
                    tags=tag_id,
                    short_description=json.dumps(oxirgi, ensure_ascii=False),
                    characteristics=app_json,
                    variations='[]',
                    variation_attributes='[]',
                    variation_colors=color_json,
                    todays_deal=1,
                    published=1,
                    featured=1,
                    unit='pcs',
                    weight=float(ves) / 1000,
                    num_of_sale=0,
                    meta_title=ann,
                    meta_description=description,
                    meta_img='',
                    pdf='',
                    slug=elem_slug,
                    earn_point=random.randint(20, 100) * 100,
                    rating=random.randint(0, 5),
                    barcode=papka,
                    digital=1,
                    file_name='',
                    file_path='',
                    created_at='2021-06-28 08:43:07',
                    updated_at='2021-06-28 08:43:07',
                    on_moderation=0,
                    is_accepted=1,
                    refundable=1,
                ).save()
                var_namee = {'uz': f'{var_a}', 'ru': f'{var_a}', 'en': f'{var_a}', 'default': f'{var_a}'}
                var_de = {'uz': f'{description}', 'ru': f'{description}', 'en': f'{description}'}
                v = VariationTranslations.objects.create(name=var_namee, description=var_de,created_at='2021-06-28 08:43:07',updated_at='2021-06-28 08:43:07')
                v.save()
                variation = Variations(
                    name=v.id,
                    lowest_price_id=0,
                    slug=elem_slug,
                    partnum=papka,
                    element_id=n.id,
                    prices=random.randint(1, 10) * 100,
                    variant='',
                    short_description=json.dumps(oxirgi, ensure_ascii=False),
                    created_at='2021-08-01 16:32:32',
                    updated_at='2021-08-01 16:32:32',
                    user_id=9,
                    num_of_sale=0,
                    qty=0,
                    rating=random.randint(0, 5),
                    thumbnail_img=photo_thum_json,
                    photos=photo_id_json,
                    color_id=color_id,
                    characteristics=None,
                    deleted_at=None,
                ).save()
                var_id = Variations.objects.filter(name=v.id)[:1].get().id
                p = Products(
                    name=n.id,
                    slug=elem_slug,
                    user_id=3,
                    added_by='seller',
                    currency_id=1,
                    price=random.randint(1, 10) * 100,
                    discount=random.randint(0, 10),
                    discount_type='percent',
                    discount_start_date=None,
                    discount_end_date=None,
                    variation_id=v.id,
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
                    element_id=n.id,
                    sku=None,
                    deleted_at=None,
                    is_quantity_multiplied=0
                ).save()
                if os.path.isfile(f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\sizes.json'):
                    zss=self.read_json(f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\sizes.json')
                    if len(zss)>1:
                        xs=0
                        fake_branchhh_id = BranchTranslations.objects.filter(name__ru=f"{single_branch_name}")[:1].get().id
                        original_branch_id = Branches.objects.filter(name=fake_branchhh_id)[:1].get().id
                        att_idd_0 = AttributeTranslations.objects.filter(name__ru="Размер")[:1].get().id
                        att_idd_1 = Attributes.objects.filter(Q(branch_id=original_branch_id) & Q(name=att_idd_0))[:1].get().id
                        Attributes.objects.filter(Q(branch_id=original_branch_id) & Q(name=att_idd_0)).update(combination=1)
                        for s in zss[1:]:
                            xs+=1
                            char_t_0_id = CharacteristicTranslations.objects.filter(name__ru=f"{s}")[:1].get().id
                            char_t_1_id = Characteristics.objects.filter(Q(name=char_t_0_id) & Q(attribute_id=att_idd_1))[:1].get().id
                            if color !="":
                                sss=ann1 + ', ' + s + ', ' +color
                            else:
                                sss=ann1 + ', ' + s

                            var_namee = {'uz': f'{sss}', 'ru': f'{sss}', 'en': f'{sss}', 'default': f'{sss}'}
                            var_de = {'uz': f'{description}', 'ru': f'{description}', 'en': f'{description}'}
                            vsz = VariationTranslations.objects.create(name=var_namee, description=var_de,created_at='2021-06-28 08:43:07',updated_at='2021-06-28 08:43:07')
                            vl_slug = self.get_slugify(f'{sss}')
                            if int(self.slug_unique_for_var(vl_slug)) != 0:
                                vl_slug = vl_slug + f'-{int(self.slug_unique_for_var(vl_slug))}'
                            vsz.save()
                            variation = Variations(
                                name=vsz.id,
                                lowest_price_id=0,
                                slug=vl_slug,
                                partnum=str(int(papka)*100000+xs),
                                element_id=n.id,
                                prices=random.randint(1, 10) * 100,
                                variant='',
                                short_description=json.dumps(oxirgi, ensure_ascii=False),
                                created_at='2021-08-01 16:32:32',
                                updated_at='2021-08-01 16:32:32',
                                user_id=9,
                                num_of_sale=0,
                                qty=0,
                                rating=random.randint(0, 5),
                                thumbnail_img=photo_thum_json,
                                photos=photo_id_json,
                                color_id=color_id,
                                characteristics=char_t_1_id,
                                deleted_at=None,
                            ).save()

            else:
                if os.path.isfile(f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\sizes.json'):
                    zss=self.read_json(f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\sizes.json')
                    if len(zss)>1:
                        xs = 0
                        fake_branchhh_id = BranchTranslations.objects.filter(name__ru=f"{single_branch_name}")[:1].get().id
                        original_branch_id = Branches.objects.filter(name=fake_branchhh_id)[:1].get().id
                        att_idd_0 = AttributeTranslations.objects.filter(name__ru="Размер")[:1].get().id
                        att_idd_1 = Attributes.objects.filter(Q(branch_id=original_branch_id) & Q(name=att_idd_0))[:1].get().id
                        Attributes.objects.filter(Q(branch_id=original_branch_id) & Q(name=att_idd_0)).update(combination=1)
                        for s in zss[1:]:
                            xs += 1
                            char_t_0_id = CharacteristicTranslations.objects.filter(name__ru=f"{s}")[:1].get().id
                            char_t_1_id = Characteristics.objects.filter(Q(name=char_t_0_id) & Q(attribute_id=att_idd_1))[:1].get().id
                            if color != "":
                                sss = ann1 + ', ' + s + ', ' + color
                            else:
                                sss = ann1 + ', ' + s

                            var_namee = {'uz': f'{sss}', 'ru': f'{sss}', 'en': f'{sss}', 'default': f'{sss}'}
                            var_de = {'uz': f'{description}', 'ru': f'{description}', 'en': f'{description}'}
                            vsz = VariationTranslations.objects.create(name=var_namee, description=var_de,
                                                                       created_at='2021-06-28 08:43:07',
                                                                       updated_at='2021-06-28 08:43:07')
                            vl_slug = self.get_slugify(f'{sss}')
                            if int(self.slug_unique_for_var(vl_slug)) != 0:
                                vl_slug = vl_slug + f'-{int(self.slug_unique_for_var(vl_slug))}'
                            vsz.save()
                            variation = Variations(
                                name=vsz.id,
                                lowest_price_id=0,
                                slug=vl_slug,
                                partnum=str(int(papka) * 100000 + xs),
                                element_id=n.id,
                                prices=random.randint(1, 10) * 100,
                                variant='',
                                short_description=json.dumps(oxirgi, ensure_ascii=False),
                                created_at='2021-08-01 16:32:32',
                                updated_at='2021-08-01 16:32:32',
                                user_id=9,
                                num_of_sale=0,
                                qty=0,
                                rating=random.randint(0, 5),
                                thumbnail_img=photo_thum_json,
                                photos=photo_id_json,
                                color_id=color_id,
                                characteristics=char_t_1_id,
                                deleted_at=None,
                            ).save()
                else:
                    atrrr = AttributeTranslations.objects.filter(name__ru=f"Объем встроенной памяти (Гб)")[:1].get().id
                    Attributes.objects.filter(name=atrrr).update(combination=1)
                    # Attributes.objects.filter(name='Максимальный объем карты памяти').update(combination=1)
                    eee_tran_id = ElementTranslations.objects.filter(name__ru=f"{ann}")[:1].get().id
                    elem_id = Elements.objects.filter(name=eee_tran_id)[:1].get().id
                    variat_json = Elements.objects.filter(id=elem_id)[:1].get().variations
                    var_json_colors = Elements.objects.filter(id=elem_id)[:1].get().variation_colors
                    element_characters = json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                    new_char = self.join_dicts(element_characters, attr_diction_umumiy)
                    # print(f'eski ---------------------{attr_diction_umumiy}\nvar_char----------{element_characters}\nnew_char---------------{new_char}')
                    Elements.objects.filter(id=elem_id).update(characteristics=json.dumps(new_char))
                    if var_json_colors != None:
                        variation_colors = json.loads(var_json_colors)
                    else:
                        variation_colors = None
                    if color != '':
                        cccc = ColorTranslations.objects.filter(name__ru=f"{color}")[:1].get().id
                        color_id = Colors.objects.filter(name=cccc)[:1].get().id
                    else:
                        color_id = None
                    categ = Elements.objects.filter(id=elem_id)[:1].get().tags
                    categories = categ.split(',')
                    if os.path.isfile(f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\extra_name.json'):
                        cate_name = self.read_json(
                            f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\extra_name.json')
                        categor_id = self.get_category_id(f'{cate_name}')
                        if str(categor_id) not in categories:
                            categ += f',{categor_id}'
                            Elements.objects.filter(id=elem_id).update(tags=categ)
                    if color_id != None:
                        if variation_colors == None:
                            variation_colors = list()
                            variation_colors.append(f'{color_id}')
                        elif f'{color_id}' not in variation_colors:
                            variation_colors.append(f'{color_id}')
                        variat_json_color1 = json.dumps(variation_colors)
                        variat_json_color = self.remove_space(variat_json_color1)
                        Elements.objects.filter(id=elem_id).update(variation_colors=variat_json_color)
                    if memory != "":
                        m_charr = CharacteristicTranslations.objects.filter(name__ru=f"{self.remove_all_spaces(memory.lower())}")[:1].get().id
                        memory_id = Characteristics.objects.filter(name=m_charr)[:1].get().id
                        attri_id = Attributes.objects.filter(name=atrrr)[:1].get().id
                        # try:
                        #     attribute_id = AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=memory_id)[:1].get().id
                        # except ObjectDoesNotExist as den:
                        #     p = AttributeCharacteristic(
                        #         attribute_id=attri_id,
                        #         characteristic_id=memory_id
                        #     ).save()
                        #     attribute_id = AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=memory_id)[:1].get().id
                    if Variations.objects.filter(Q(element_id=elem_id) & Q(color_id=color_id) & Q(characteristics=memory_id)).exists():
                        continue
                    if variat_json == '[]':
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
                            elem_char_m = json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                            aa1 = list(elem_char_m[f'{attri_id}'])
                            if f'{memory_id}' not in aa1:
                                aa1.append(f'{memory_id}')
                            elem_char_m[f'{attri_id}'] = aa1
                            aa2 = json.dumps(elem_char_m)
                            Elements.objects.filter(id=elem_id).update(characteristics=aa2, variations=a2,variation_attributes=m2)
                    else:
                        if memory != "":
                            a1 = json.loads(variat_json)
                            if f'{attri_id}' in a1.keys():
                                a2 = list(a1[f'{attri_id}'])
                                if f'{memory_id}' not in a2:
                                    a2.append(f'{memory_id}')
                                    a1[f'{attri_id}'] = a2
                                    elem_char_m = json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                                    aa1 = list(elem_char_m[f'{attri_id}'])
                                    if f'{memory_id}' not in aa1:
                                        aa1.append(f'{memory_id}')
                                    elem_char_m[f'{attri_id}'] = aa1
                                    aa2 = json.dumps(elem_char_m)
                                    Elements.objects.filter(id=elem_id).update(characteristics=aa2,variations=json.dumps(a1))
                            elif f'{attri_id}' not in a1.keys():
                                d = []
                                for aak in a1.keys():
                                    d.append(f'{aak}')
                                elem_char_m = json.loads(Elements.objects.filter(id=elem_id)[:1].get().characteristics)
                                aa1 = list(elem_char_m[f'{attri_id}'])
                                if f'{memory_id}' not in aa1:
                                    aa1.append(f'{memory_id}')
                                elem_char_m[f'{attri_id}'] = aa1
                                aa2 = json.dumps(elem_char_m)
                                a1[f'{attri_id}'] = list(f'{memory_id}')
                                Elements.objects.filter(id=elem_id).update(characteristics=aa2, variations=json.dumps(a1),variation_attributes=json.dumps(d))

                    # variatsiya=''
                    # if variat_json != None:
                    #     if memory != "":
                    #         variatsiya=variat_json.split(',')
                    #         print(variatsiya)
                    #         if str(attribute_id) not in variatsiya:
                    #             variat_json+=','+str(attribute_id)
                    #             Elements.objects.filter(id=elem_id).update(variations=variat_json, variation_attributes=variat_json)
                    # elif variat_json == None:
                    #     if memory != "":
                    #         variatsiya+=str(attribute_id)
                    #         # print(variatsiya)
                    #         Elements.objects.filter(id=elem_id).update(variations=variatsiya, variation_attributes=variatsiya)

                    phot_list = ''
                    photo_thum = ''

                    if not VariationTranslations.objects.filter(name__ru=f"{var_name}").exists():
                        for i in range(1, 50):
                            if os.path.isfile(
                                    f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\images\{papka}-{i}.jpg'):
                                file_size = os.path.getsize(
                                    f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\images\{papka}-{i}.jpg')
                                file_name = self.hash_and_move(f'{papka}-{i}',
                                                               f'{os.path.dirname(absolute_path)}\{nam111}\{papka}\images\{papka}-{i}.jpg')
                                photos_id = self.uploads(f'{papka}-{i}', file_name, file_size)
                                if i == 1:
                                    photo_thum += f'{photos_id}'
                                else:
                                    if i == 2:
                                        phot_list += f'{photos_id}'
                                    else:
                                        phot_list += f',{photos_id}'
                            else:
                                break
                        phot_list_json = phot_list
                        photo_thum_json = photo_thum
                        var_slug = self.get_slugify(f'{var_name}')
                        if int(self.slug_unique_for_var(var_slug)) != 0:
                            var_slug = var_slug + f'-{int(self.slug_unique_for_var(var_slug))}'
                        v_name = {'uz': f'{var_name}', 'ru': f'{var_name}', 'en': f'{var_name}', 'default': f'{var_name}',
                                  'meta_title': f'{var_name}'}
                        v_descrip = {'uz': f'{description}', 'ru': f'{description}', 'en': f'{description}'}
                        vv = VariationTranslations(name=v_name, description=v_descrip, created_at='2021-09-13 20:22:42',updated_at='2021-09-13 20:22:42')
                        vv.save()
                        if memory == "":
                            variation = Variations(
                                name=vv.id,
                                lowest_price_id=0,
                                slug=var_slug,
                                partnum=papka,
                                element_id=elem_id,
                                prices=random.randint(1, 10) * 100,
                                variant='',
                                short_description=json.dumps(oxirgi, ensure_ascii=False),
                                created_at='2021-08-01 16:32:32',
                                updated_at='2021-08-01 16:32:32',
                                user_id=9,
                                num_of_sale=random.randint(1, 100),
                                qty=0,
                                rating=random.randint(0, 5),
                                thumbnail_img=photo_thum_json,
                                photos=phot_list_json,
                                color_id=color_id,
                                characteristics=None,
                                deleted_at=None,
                            ).save()
                        else:
                            # attri_id=Attributes.objects.filter(name='Объем встроенной памяти (Гб)')[:1].get().id
                            mmmm = CharacteristicTranslations.objects.filter(
                                name__ru=f"{self.remove_all_spaces(memory.lower())}")[:1].get().id
                            memory_id1 = Characteristics.objects.filter(name=mmmm)[:1].get().id
                            # try:
                            #     attribute_id = AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=memory_id)[:1].get().id
                            # except ObjectDoesNotExist as den:
                            #     p = AttributeCharacteristic(
                            #         attribute_id=attri_id,
                            #         characteristic_id=memory_id
                            #     ).save()
                            #     attribute_id = AttributeCharacteristic.objects.filter(attribute_id=attri_id,characteristic_id=memory_id)[:1].get().id

                            print(f'memory_id={memory_id1}')
                            variation = Variations(
                                name=vv.id,
                                lowest_price_id=0,
                                slug=var_slug,
                                partnum=papka,
                                element_id=elem_id,
                                prices=random.randint(1, 10) * 100,
                                variant='',
                                short_description=json.dumps(oxirgi, ensure_ascii=False),
                                created_at='2021-08-01 16:32:32',
                                updated_at='2021-08-01 16:32:32',
                                user_id=9,
                                num_of_sale=random.randint(1, 100),
                                qty=0,
                                rating=random.randint(0, 5),
                                thumbnail_img=photo_thum_json,
                                photos=phot_list_json,
                                color_id=color_id,
                                characteristics=memory_id1,
                                deleted_at=None,
                            ).save()




class Command(BaseCommand):
    help='Parsing Wildberries'
    def handle(self, *args, **options):
        p=WildberiesParser()
        p.put_attributes(cate_name={'Планшеты': 'https://www.wildberries.ru/catalog/elektronika/planshety'},number=2)
        # p.element(cate_name={'Планшеты': 'https://www.wildberries.ru/catalog/elektronika/planshety'},number=2)
 #



 # p.put_branch(cate_name={'Планшеты': 'https://www.wildberries.ru/catalog/elektronika/planshety'},number=2)






