from bs4 import  BeautifulSoup
import os
from django.core.management.base import BaseCommand
import json
import os

class a:
    def p(self):
        absolute_path = os.path.abspath(__file__)
        a=self.read_json(f"{os.path.dirname(absolute_path)}\Фрукты\Яблоки\\1\product_characters.json")
        for k,v in a['Общие характеристики'].items():
            print(k,v)
        
        
    
    def read_file(self,path):
        file = open(path, "r",encoding='utf-8')
        data = file.read()
        file.close()
        return data
    
    def read_json(self,path):
        return json.loads(self.read_file(path))
        # for a in text:
        #     print(f'{a.get_text(text=True)}')
            


class Command(BaseCommand):
    def handle(self, *args, **options):
        p=a()
        p.p()