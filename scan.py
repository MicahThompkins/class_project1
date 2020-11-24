import json
import sys
import time
import subprocess


print("hello world")
command_input = sys.argv
timeout_num = 1
input_file = str(command_input[1])
output_file = str(command_input[2])

print("after inout")
# output_dictonary = {}
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
        output_dictonary[func] = eval(func + "('" + url + "')")
    return output_dictonary
    # TODO add try catch if command line tool missing and timeoutexpired

def scan_time(url):
    return time.time()


def ipv4_addresses(url):
    dns_resolvers = ["208.67.222.222", "1.1.1.1", "8.8.8.8", "8.26.56.26", "9.9.9.9", "64.6.65.6", "91.239.100.100", "185.228.168.168", "77.88.8.7", "156.154.70.1", "198.101.242.72", "176.103.130.130"]
    ip_addys = []
    for dns in dns_resolvers:
        try:
            result = subprocess.check_output(["nslookup", url, dns], timeout=timeout_num).decode("utf-8")
        except subprocess.TimeoutExpired:
            # print("timing out")
            continue
        except subprocess.CalledProcessError:
            # print("calledProcesserror")
            continue
        split_result = result.split("Name")
        del split_result[0]
        for address in split_result:
            find_index = address.find("Address: ")
            addy = address[find_index + 9:]
            addy = addy.strip()
            if addy not in ip_addys:
                ip_addys.append(addy)
    return ip_addys


def ipv6_addresses(url):
    dns_resolvers = ["208.67.222.222", "1.1.1.1", "8.8.8.8", "8.26.56.26", "9.9.9.9", "64.6.65.6", "91.239.100.100", "185.228.168.168", "77.88.8.7", "156.154.70.1", "198.101.242.72", "176.103.130.130"]
    ip_addys = []
    for dns in dns_resolvers:
        try:
            result = subprocess.check_output(["nslookup", "-type=AAAA", url, dns],
                                             timeout=timeout_num).decode("utf-8")
        except subprocess.TimeoutExpired:
            # print("timing out")
            continue
        except subprocess.CalledProcessError:
            # print("calledProcesserror")
            continue
        if "Can't find" in result:
            continue
        else:
            split_result = result.split("has AAAA address")
            del split_result[0]
            for address in split_result:
                addy = address.split("\n")
                addy = addy[0].strip()
                if addy not in ip_addys:
                    ip_addys.append(addy)
    return ip_addys



def http_server(url):

    try:
        result = subprocess.check_output(["curl", "-I", "--http2", url],
                                         timeout=timeout_num).decode("utf-8")
    except subprocess.TimeoutExpired:
        # print("timing out")
        return False
    except subprocess.CalledProcessError:
        # print("calledProcesserror")
        return False
    split_result = result.split("Server: ")
    del split_result[0]
    server = split_result[0].split("\r\n")
    answer = server[0]
    return answer


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