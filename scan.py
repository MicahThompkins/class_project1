import json
import sys
import time
import subprocess

print("hello world")
command_input = sys.argv
timeout_num = 1
input_file = str(command_input[1])
output_file = str(command_input[2])


class ScanClass:

    print("after inout")
    # output_dictonary = {}
    # results_to_pass = ""
    def __init__(self, input_file, output_file):
        print("in main")
        file = open(input_file, 'r')
        file_lines = file.readlines()
        output_dictonary = {}
        self.result_to_pass = ""
        self.hsts_bool = False
        for line in file_lines:
            line = line.rstrip()
            output = self.scan(line)
            output_dictonary[line] = output
        file.close()
        with open(output_file, 'w') as f:
            json.dump(output_dictonary, f, sort_keys=False, indent=4)
            f.close()


    def scan(self, url):
        func_names = ["scan_time", "ipv4_addresses", "ipv6_addresses", "http_server", "insecure_http", "redirect_to_https", "hsts", "tls_versions", "root_ca", "rdns_names", "rtt_range", "geo_locations"]
        # func_names = ["scan_time", "ipv4_addresses", "ipv6_addresses", "http_server", "redirect_to_https", "hsts", "tls_versions", "root_ca", "rdns_names", "rtt_range", "geo_locations"]
        output_dictonary = {}
        for func in func_names:
            output_dictonary[func] = eval('self.' + func + "('" + url + "')")
        return output_dictonary
        # TODO add try catch if command line tool missing and timeoutexpired

    def scan_time(self, url):
        return time.time()

    def ipv4_addresses(self, url):
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

    def ipv6_addresses(self, url):
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

    def http_server(self, url):
        url = "http://"  + url
        try:
            result = subprocess.check_output(["curl", "-I", "--http2", url],
                                             timeout=timeout_num).decode("utf-8")
        except subprocess.TimeoutExpired:
            # print("timing out")
            # output_dictonary[url]["insecure_http"] = False
            print("returning none after timeoutexpired in http: server: ", url)
            return None
        except subprocess.CalledProcessError:
            # print("calledProcesserror")
            # output_dictonary[url]["insecure_http"] = False
            print("returning none after calledprocesserror in http: server: ", url)
            return None
        # print(result)
        self.result_to_pass = result
        split_result = result.split("Server: ")
        if len(split_result) == 1:
            split_result = result.split("server: ")
            if len(split_result) == 1:
                #TODO check if this works specail json null
                return None
        del split_result[0]
        server = split_result[0].split("\r\n")
        answer = server[0]
        return answer

    def insecure_http(self, url):
        # print("self.result_to_pass: ", self.result_to_pass)
        if self.result_to_pass != "":
            # self.result_to_pass = ""
            return True
        else:
            # self.result_to_pass = ""
            return False

    def redirect_helper(self, location):
        count = 1
        while count < 10:
            try:
                result = subprocess.check_output(["curl", "-I", "--http2", location],
                                                 timeout=timeout_num).decode("utf-8")
            except subprocess.TimeoutExpired:
                return False
            except subprocess.CalledProcessError:
                return False
            location_split = result.split("Location: ")
            if len(location_split) > 1:
                del location_split[0]
                location_split = location_split[0].split("\r\n")
                location = location_split[0]
                if "https://" in location:
                    self.redirect_hsts_helper(location)
                    return True
                else:
                    count = count + 1
                    if count == 10:
                        return False

            else:
                return False

    def redirect_hsts_helper(self, url):
        try:
            result = subprocess.check_output(["curl", "-I", "--http2", url],
                                             timeout=timeout_num).decode("utf-8")
        except subprocess.TimeoutExpired:
            self.hsts_bool = False
            return False
        except subprocess.CalledProcessError:
            self.hsts_bool = False
            return False
        if "strict-transport-security: " in result:
            self.hsts_bool = True
            return True

    def redirect_to_https(self, url):
        if self.result_to_pass != "":
            # TODO if 200 OK shows up elsewhere could find index of http and index of 200 ok and check to make sure distance is small
            if "200 OK" in self.result_to_pass:
                self.result_to_pass = ""
                return False
            else:
                location_split = self.result_to_pass.split("Location: ")
                if len(location_split) > 1:
                    del location_split[0]
                    location_split = location_split[0].split("\r\n")
                    location = location_split[0]
                    if "https://" in location:
                        self.result_to_pass = ""
                        self.redirect_hsts_helper(location)
                        return True
                    else:
                        return_val = self.redirect_helper(location)
                        self.result_to_pass = ""
                        return return_val
                else:
                    self.result_to_pass = ""
                    return False
        else:
            self.result_to_pass = ""
            return False

    def hsts(self, url):
        if self.hsts_bool:
            self.hsts_bool = False
            return True
        else:
            return False

    def tls_versions(self, url):
        return "test tls"

    def root_ca(self, url):
        return "test root"

    def rdns_names(self, url):
        return "test rdns"

    def rtt_range(self, url):
        return "test rtt"

    def geo_locations(self, url):
        return "test geo"


s = ScanClass(input_file, output_file)