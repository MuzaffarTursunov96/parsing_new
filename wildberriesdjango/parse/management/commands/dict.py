# a={'1':['12','56'],'2':['45','2']}
# b={'1':['12'],'8':['6']}
# c={}
# def merge_dicts(d1, d2):
#     k1=[]
#     k2=[]
#     for k in d1.keys():
#         k1.append(k)
#     for k in d2.keys():
#         k2.append(k)
#     att_rt=[]
#     for k in k1:
#         if k not in k2:
#             list_d1=d1[f'{k}']
#             d2[f'{k}']=list_d1
#             att_rt.append(k)
#         else:
#             a=d1[f'{k}']
#             b=d2[f'{k}']
#             resultList= list(set(a) | set(b))
#             d2[f'{k}']=resultList
#     return {'obshiy':d2,'list':att_rt}
#
# for a in merge_dicts(b,a)['list']:
#     print(a)
# print(merge_dicts(b,a)['list'])

# a=['a','1','3']
# b=['a','45','6','3']
# resultList= list(set(a) | set(b))
# print(resultList)
# a='sfxfxxhxfh;vuyvkvuvuv;guyvyuvvvvvnvv;'
# a=a.split(';')[1]
# print(a)
from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
print(similar(a='Шпилька-спиралька 4 шт.',b='Шпилька крепежная'))

