import random
import time
from collections import namedtuple
from bs4 import  BeautifulSoup
import  requests
import os
import json
import socket


all_dictionary={
    'Смарт часы и аксессуары':'https://www.wildberries.ru/catalog/elektronika/smart-chasy?sort=popular&'
}
all_pages=[229]



class Parse_All:

    def __init__(self):
        self.session = requests.Session()
        self.useragents=[
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
        self.session.headers = {
            'User-Agent': f'{random.choices(self.useragents)}'
        }
    def check_exists(self, cate_name, prod_name):
        absolute_path = os.path.abspath(__file__)
        filees = os.path.isfile(f'{os.path.dirname(absolute_path)}\{cate_name}\{prod_name}\product_detail.html')
        return filees


    def test_request(self, url, retry=5):
        try:
            response = self.session.get(url)
        except Exception as ex:
            if retry:
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


    def get_dict(self, all_dict, all_pages):
        count = 0
        absolute_path = os.path.abspath(__file__)
        for category_name, category_href in all_dict.items():
            if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{category_name}'):
                self.cate_dir(category_name)
            else:
                continue

            for i in range(1, all_pages[count] + 1):
                if not os.path.isfile(f"{os.path.dirname(absolute_path)}\{category_name}\{i}.html"):
                    response = self.test_request(f'{category_href}page={i}')
                    source = response.text
                    with open(f"{os.path.dirname(absolute_path)}\{category_name}\{i}.html", 'w', encoding='utf-8') as file:
                        file.write(source)
            count += 1

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


    def get_path1(self,cate_name,number):
        absolute_path = os.path.abspath(__file__)
        count=0
        for category_name, category_href in cate_name.items():
            for i in range(1, number[count]+1):
                with open(f"{os.path.dirname(absolute_path)}\{category_name}\{i}.html", encoding='utf-8') as file:
                    source = file.read()
                self.product_css1(source, category_name)
            count+=1

    def product_css1(self,source, category_name):
        soup = BeautifulSoup(source, 'lxml')
        all_product = soup.find_all(class_='product-card j-card-item')
        for product_hrefs in all_product:
            product_href = product_hrefs.find(class_='j-open-full-product-card').get('href')
            papka = self.nom(product_href)
            print(papka)
            absolute_path = os.path.abspath(__file__)
            if self.prod_papka_yaratish(category_name, papka):
                parent_dir = f'{os.path.dirname(absolute_path)}\{category_name}'
                path = os.path.join(parent_dir, f'{papka}')
                os.mkdir(path)
                par_img = f'{os.path.dirname(absolute_path)}\{category_name}\{papka}'
                if not os.path.isdir(f'{os.path.dirname(absolute_path)}\{category_name}\{papka}\images'):
                    path_img = os.path.join(par_img, 'images')
                    os.mkdir(path_img)

            if self.check_exists(category_name, papka):
                continue
            else:
                response1 = self.test_request(f'https://www.wildberries.ru{product_href}')
                time.sleep(1)
                print(socket.gethostbyname(socket.gethostname()))
                source1 = response1.text
                with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\product_detail.html", 'w', encoding='utf-8') as file:
                    file.write(source1)

            with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\product_detail.html",
                      encoding='utf-8') as file:
                soup = file.read()
            source = BeautifulSoup(soup, 'lxml')
            brand_img_href = source.find(class_='same-part-kt__brand-logo').find('img').get('src')
            product_brand = source.find(class_='same-part-kt__header').find('span').get_text()
            if product_brand[-1:] == '.':
                product_brand_nam = product_brand.replace('.', '')
            else:
                product_brand_nam = product_brand

            if '/' in product_brand_nam:
                product_brand_name = product_brand_nam.replace('/', '')
            else:
                product_brand_name = product_brand_nam

            if brand_img_href != None:
                brand1 = self.test_request(f'https:{brand_img_href}')
                time.sleep(0.3)
                brand = brand1.content
                b_name =product_brand_name
                with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{b_name}.jpg",
                          'wb') as file:
                    file.write(brand)
                brand_name='brand'
                brand_json=json.dumps(product_brand_name)
                with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\{brand_name}.json", 'w',encoding='utf-8') as file:
                        json.dump(brand_json, file, indent=4, ensure_ascii=False)

            if self.check_img_dir(category_name, papka, 'images'):
                prod_images = source.find(class_='same-part-kt').find(class_='swiper-wrapper').find_all('li')
                count_img = 1
                for prod_image in prod_images:
                    if 'slide--video' in prod_image['class']:
                        continue
                    else:
                        image = prod_image.find('img').get('src')
                        req_img = self.test_request(f'https:{str(image[0:22])}big{str(image[24:])}').content
                        with open(f"{os.path.dirname(absolute_path)}\{category_name}\{papka}\images\{papka}-{count_img}.jpg", 'wb') as file:
                            file.write(req_img)
                        count_img += 1
                    time.sleep(0.5)


if __name__ == "__main__":
    p=Parse_All()
    p.get_dict(all_dictionary,all_pages)
    p.get_path1(all_dictionary,all_pages)