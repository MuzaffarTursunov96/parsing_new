# import time
#
# import  requests
# import  os
# import random
#
# user_agent_lists = [
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246 ',
#     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
#     'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
#     'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'
# ]
#
# headers = {
#     'Accept': '*/*',
#     'User-Agent': f'{random.choice(user_agent_lists)}'
# }
# cookie = {
#     'cookie': 'cookie: uid=08fbd572-9de1-487f-85e2-558495e241ab; uid3pd=4530643d-44a9-4215-aaef-254f3d061cfb'
# }
# for i in range(1,5):
#     absolute_path = os.path.abspath(__file__)
#     req=requests.get(f'https://esavdo.uz/elektronika/smartfony?price_from=0&price_to=99000000&page={i}',headers=headers)
#     a=req.text
#
#     with open(f"{os.path.dirname(absolute_path)}\{i}.html",'w',encoding='utf-8')as file:
#         file.write(a)

# title.encode('latin1').decode('cp1252').encode('UTF-8')

# a={'12':[],'56':[45,622]}
# b={'167':['1370','1372'],'45':['457','654615']}
# if '45' in b.keys():
#     print(True)
# else:
#     print(False)

# print(b.keys())
import shutil
a='6098602'
b='1'
shutil.copy2(f'd:\django\wildberriesdjango\parse\management\commands\Планшеты\{a}\images\{b}.jpg', f'd:\django\wildberriesdjango\parse\sm.jpg') # complete target filename given
# shutil.copy2('/src/file.ext', '/dst/dir') # target filename is /dst/dir/file.ext