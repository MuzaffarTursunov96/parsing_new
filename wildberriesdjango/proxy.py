# import requests
# proxy={
#     'http':'177.244.36.134:8080',
#     # '113.130.126.2':'31932',
#     # '194.87.102.116':'	81',
#     # '65.21.58.194':'80',
#     # '94.74.132.129':'808',
#     # '196.214.185.86':'80',
#     # '58.97.193.228':'55443',
#     # '177.244.36.134':'8080',
#     # '221.120.210.211':'39617',
#     # '159.89.119.77':'8080'
# }
# url='https://httpbin.org/ip'
# response=requests.get(url,proxies=proxy)
# print(response.text)

import argon2, binascii
a='password'
arr = bytes(a, 'utf-8')
hash = argon2.hash_password_raw(
    time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32,
    password=arr, salt=b'some more salt', type=argon2.low_level.Type.ID)
a=str(binascii.hexlify(hash))[2:-1]
print(a)