import json
import time
import sys
import subprocess
# print(str(time.time()))
result = subprocess.check_output(["nslookup", "-type=AAAA", "google.com", "8.8.8.8"],
                                 timeout=2).decode("utf-8")
print(result)
# split_result = result.split("Name")
# del split_result[0]
# print(split_result)
# find_index = split_result[0].find("Address: ")
# # print(find_index)
# address = split_result[0][find_index + 9:]
#
# print(address)
# address = address.strip()
#
# print(address)
# print(type(address))
# test_arr = [address]
# print(test_arr)
# print(split_result)
# print(result)
# print(type(result))