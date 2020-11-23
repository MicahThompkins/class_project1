import json
import sys
import time
print("hello world")
command_input = sys.argv

input_file = str(command_input[1])
output_file = str(command_input[2])

print("after inout")

def main(input_file, output_file):
    print("in main")
    file = open(input_file, 'r')
    file_lines = file.readlines()
    output_dictonary = {}
    for line in file_lines:
        line = line.rstrip()
        output = scan(line)
        output_dictonary[line] = output
    file.close()
    with open(output_file, 'w') as f:
        json.dump(output_dictonary, f, sort_keys=False, indent=4)
        f.close()


def scan(url):
    func_names = ["scan_time", "ipv4_addresses", "ipv6_addresses", "http_server", "insecure_http", "redirect_to_https", "hsts", "tls_versions", "root_ca", "rdns_names", "rtt_range", "geo_locations"]
    output_dictonary = {}
    for func in func_names:
        output_dictonary[func] = eval(func + "('" +  url + "')")
    return output_dictonary


def scan_time(url):
    return time.time()


def ipv4_addresses(url):
    return "test ipv4"


def ipv6_addresses(url):
    return "test ipv6"


def http_server(url):
    return "test http_ser"


def insecure_http(url):
    return "test insecrue"


def redirect_to_https(url):
    return "test redirect"


def hsts(url):
    return "test hsts"


def tls_versions(url):
    return "test tls"


def root_ca(url):
    return "test root"


def rdns_names(url):
    return "test rdns"


def rtt_range(url):
    return "test rtt"


def geo_locations(url):
    return "test geo"

main(input_file, output_file)