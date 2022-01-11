
# import argon2, binascii

# hash = argon2.hash_password_raw(
#     time_cost=16, memory_cost=4096, parallelism=1, hash_len=16,
#     password=b'Honor', salt=b'muzaffar*96#', type=argon2.low_level.Type.ID)
# a=binascii.hexlify(hash)
# print(f"Argon2 raw hash:{a}" )

# # argon2Hasher = argon2.PasswordHasher(
# #     time_cost=16, memory_cost=2**15, parallelism=2, hash_len=32, salt_len=16)
# # hash = argon2Hasher.hash("password")
# # print("Argon2 hash (random salt):", hash)

# # verifyValid = argon2Hasher.verify(hash, "password")
# # print("Argon2 verify (correct password):", verifyValid)

# # try:
# #     argon2Hasher.verify(hash, "wrong123")
# # except:
# #     print("Argon2 verify (incorrect password):", False)

# import json
# import os

# absolute_path = os.path.abspath(__file__)
# name='brand'
# with open(f"{os.path.dirname(absolute_path)}\{name}.json", 'r') as j:
#     json_data = json.load(j)

# a=json.loads(json_data)
# print(a)

ism={'muzaffar':1996}
print(find('a'))