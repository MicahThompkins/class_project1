import json
import time
import sys
import subprocess
# import requests
import http

# import scan
# print(str(time.time()))

## rdns_names done
# face_book_ip4s = ["157.240.18.35", "157.240.2.35", "69.171.250.35", "31.13.67.35", "157.240.195.35", "157.240.1.35"]
# steve = "54.245.121.172"
# error_addy = "104.28.4.211"
# command_arr = ["nslookup", "-type=PTR", error_addy]
#
# result = ""
# try:
#     result = subprocess.check_output(command_arr,
#                                      stderr = subprocess.STDOUT, timeout=2).decode("utf-8")
# except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
#     result = str(e)
#     print("e:", e)
#     print(e.output)
#     if "server can't find" in str(e.output):
#         print("it worked")
# if result != "":
#     print(result)
#     split_result = result.split("name = ")
#     print(split_result)
#     if len(split_result) > 1:
#         del split_result[0]
#         name_split = split_result[0].split("\n\n")
#         name = name_split[0]
#         if name[-1] == ".":
#             name = name[:-1]
#             print(name)

#NEED to get last line

# Certificate chain
#  0 s:/CN=stevetarzia.com
#    i:/C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X3
#  1 s:/C=US/O=Let's Encrypt/CN=Let's Encrypt Authority X3
#    i:/O=Digital Signature Trust Co./CN=DST Root CA X3

# input_arr = [5] * 10
# print(input_arr)

## ROOT_CA stuff
# command = "openssl s_client -connect amazon.com:443"
# command_arr = ["openssl", "s_client", "-connect", "amazon.com:443"]
# try:
#     result = subprocess.check_output(command_arr, input = "", stderr=subprocess.STDOUT,
#                                     timeout=5).decode("utf-8")
# except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
#     result = str(e)
#     print("e:", e)
#     print(e.output)
#
#
#
# print("result: \n", result)
# split_result = result.split("O = ")
# if len(split_result) > 1:
#     del split_result[0]
#     root_ca_split1 = split_result[0].split("CN = ")
#     root_ca_split = root_ca_split1[0].split("OU = ")
#     root_ca_first = root_ca_split[0]
#     index_of_last_comma = root_ca_first.rfind(",")
#     root_ca = root_ca_first[:index_of_last_comma]
#     print("Root CA: ", root_ca)

## TLS versions 1_3
# result = ""
# info = "echo | openssl s_client -tls1_3 -connect tls13.cloudflare.com:443"
# try:
#     result = subprocess.check_output(["openssl", "s_client", "-tls1_3", "-connect", "tls131.cloudfare.com:443"],
#                                     timeout=2).decode("utf-8")
# except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
#     result = str(e)
#     print("e:", e)
#
#
# print(result)
# if "returned non-zero exit status 1" in result:
#     print("it worked")
# else:
#     print("it didnt work")

## TLS_versions early
# result = ""
# command = "nmap --script ssl-enum-ciphers -p 443 reddit.com"
#
# try:
#     result = subprocess.check_output(["nmap", "--script", "ssl-enum-ciphers", "-p", "443", "en.wikipedia.org"],
#                                     timeout=10).decode("utf-8")
# except (FileNotFoundError, OSError) as e:
#     print("excepted: ", e)
#
# def tls_nmap_helper(result, return_arr, tls_ver):
#     split_result = result.split(tls_ver)
#     if len(split_result) > 1:
#         del split_result[0]
#         return_arr.append(tls_ver)
#         return split_result[0]
#     else:
#         return result
#
# tls_vers = ["TLSv1.0", "TLSv1.1", "TLSv1.2"]
# if result != "":
#     return_arr = []
#     for tls in tls_vers:
#         print("tls: ", tls)
#         result = tls_nmap_helper(result, return_arr, tls)
#     print("return_arr: ", return_arr)


# print(result)

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
