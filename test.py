import json
import time
import sys
import subprocess
import requests
import http

# import scan
# print(str(time.time()))

result = subprocess.check_output(["curl", "-I", "--http2", "https://www.amazon.com"],
                                 timeout=2).decode("utf-8")

print(result)

## Redirect_hst_helper
# location_split = result.split("Location: ")
# del location_split[0]
# location = location_split[0].split("\r\n")
# print(location)

## http_server test code below
# print("result: ", result)
# split_result = result.split("Server: ")
# print(split_result)
# del split_result[0]
# server = split_result[0].split("\r\n")
# print(server)
# answer = server[0]
# print(answer)

## IPV6 test code below
# result = subprocess.check_output(["nslookup", "-type=AAAA", "google.com", "8.8.8.8"],
#                                  timeout=2).decode("utf-8")
# print(result)
# if "Can't find" in result:
#     print(True)
# else:
#     print(False)
# split_result = result.split("has AAAA address")
# print(split_result)
# del split_result[0]
# address = split_result[0].split("\n")
# address[0] = address[0].strip()
# print(address)


## IPV4 test code below
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
# print(split_result)source tutorial-env/bin/activate
# print(result)
# print(type(result))