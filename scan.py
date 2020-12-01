import json
import sys
import time
import subprocess
import maxminddb

print("hello world")
command_input = sys.argv
timeout_num = 2
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
        self.output_dictonary = {}
        self.scan_output_dictonary = {}
        self.result_to_pass = ""
        self.hsts_bool = False
        for line in file_lines:
            line = line.rstrip()
            output = self.scan(line)
            self.output_dictonary[line] = output
        file.close()
        with open(output_file, 'w') as f:
            json.dump(self.output_dictonary, f, sort_keys=False, indent=4)
            f.close()


    def scan(self, url):
        func_names = ["scan_time", "ipv4_addresses", "ipv6_addresses", "http_server", "insecure_http", "redirect_to_https", "hsts", "tls_versions", "root_ca", "rdns_names", "rtt_range", "geo_locations"]
        func_names = ["scan_time", "tls_versions"]  # , "rdns_names"]
        # func_names = ["scan_time", "ipv4_addresses", "ipv6_addresses", "http_server", "redirect_to_https", "hsts", "tls_versions", "root_ca", "rdns_names", "rtt_range", "geo_locations"]
        # output_dictonary = {}
        self.scan_output_dictonary = {}
        for func in func_names:
            print(url, func)
            try:
                self.scan_output_dictonary[func] = eval('self.' + func + "('" + url + "')")
            except (FileNotFoundError, OSError) as e:
                print("exception caught: ", e)
                error_out = func + " is not able to run due to missing command line tool"
                # print(error_out, file=sys.stderr)
                sys.stderr.write(error_out)
        return self.scan_output_dictonary

    def subprocess_caller(self, args, timeout_input):
        result = ""
        count = 0
        # TODO if slow add this code for rdns_names: but should be fine
        # if "server can't find" in str(e.output):
        #     print("it worked")
        while True:
            try:
                result = subprocess.check_output(args, timeout=timeout_input).decode("utf-8")
            except subprocess.TimeoutExpired as e:
                # print("timing out for command: ", args[0], " at site: ", args[-1])
                # print(e)
                if count > 1:
                    break
                else:
                    count += 1
            except subprocess.CalledProcessError as e:
                # print("called_process_Error for command: ", args[0], "at site: ", args[-1])
                # print(e)
                if count > 1:
                    break
                else:
                    count += 1
            if result != "":
                break
        return result


    def scan_time(self, url):
        return time.time()

    def ipv4_addresses(self, url):
        dns_resolvers = ["208.67.222.222", "1.1.1.1", "8.8.8.8", "8.26.56.26", "9.9.9.9", "64.6.65.6", "91.239.100.100", "185.228.168.168", "77.88.8.7", "156.154.70.1", "198.101.242.72", "176.103.130.130"]
        ip_addys = []
        for dns in dns_resolvers:
            # try:
            #     result = subprocess.check_output(["nslookup", url, dns], timeout=timeout_num).decode("utf-8")
            # except subprocess.TimeoutExpired:
            #     # print("timing out")
            #     continue
            # except subprocess.CalledProcessError:
            #     # print("calledProcesserror")
            #     continue
            # print("url, dns: ", url, dns)
            args = ["nslookup", url, dns]
            result = self.subprocess_caller(args, timeout_num)
            if result == "":
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
            # try:
            #     result = subprocess.check_output(["nslookup", "-type=AAAA", url, dns],
            #                                      timeout=timeout_num).decode("utf-8")
            # except subprocess.TimeoutExpired:
            #     # print("timing out")
            #     continue
            # except subprocess.CalledProcessError:
            #     # print("calledProcesserror")
            #     continue
            args = ["nslookup", "-type=AAAA", url, dns]
            result = self.subprocess_caller(args, timeout_num)
            if "Can't find" in result or result == "":
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
        # try:
        #     result = subprocess.check_output(["curl", "-I", "--http2", url],
        #                                      timeout=timeout_num).decode("utf-8")
        # except subprocess.TimeoutExpired:
        #     # print("timing out")
        #     # output_dictonary[url]["insecure_http"] = False
        #     print("returning none after timeoutexpired in http: server: ", url)
        #     return None
        # except subprocess.CalledProcessError:
        #     # print("calledProcesserror")
        #     # output_dictonary[url]["insecure_http"] = False
        #     print("returning none after calledprocesserror in http: server: ", url)
        #     return None
        args = ["curl", "-I", "--http2", url]
        result = self.subprocess_caller(args, timeout_num)
        if result != "":
            # print(result)
            self.result_to_pass = result
            split_result = result.split("Server: ")
            if len(split_result) == 1:
                split_result = result.split("server: ")
                if len(split_result) == 1:
                    return None
            del split_result[0]
            server = split_result[0].split("\r\n")
            answer = server[0]
            return answer
        else:
            return None

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
            args = ["curl", "-I", "--http2", location]
            result = self.subprocess_caller(args, timeout_num)
            # try:
            #     result = subprocess.check_output(["curl", "-I", "--http2", location],
            #                                      timeout=timeout_num).decode("utf-8")
            # except subprocess.TimeoutExpired:
            #     return False
            # except subprocess.CalledProcessError:
            #     return False
            if result == "":
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
        args = ["curl", "-I", "--http2", url]
        result = self.subprocess_caller(args, timeout_num)
        # try:
        #     result = subprocess.check_output(["curl", "-I", "--http2", url],
        #                                      timeout=timeout_num).decode("utf-8")
        # except subprocess.TimeoutExpired:
        #     self.hsts_bool = False
        #     return False
        # except subprocess.CalledProcessError:
        #     self.hsts_bool = False
        #     return False
        if result == "":
            self.hsts_bool = False
            return False
        #TODO add server header check and change
        if "strict-transport-security: " in result:
            self.hsts_bool = True
            return True

    def redirect_to_https(self, url):
        if self.result_to_pass != "":
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

    def tls_nmap_helper(self, result, return_arr, tls_ver):
        split_result = result.split(tls_ver)
        if len(split_result) > 1:
            del split_result[0]
            return_arr.append(tls_ver)
            return split_result[0]
        else:
            return result

    def tls_1_3_helper(self, url):
        url_string = url + ":443"
        args = ["openssl", "s_client", "-tls1_3", "-connect", url_string]
        count = 0
        tls_3_in = False
        result = ""
        while True:
            try:
                result = subprocess.check_output(args,
                                                 timeout=2).decode("utf-8")
                break
            except subprocess.TimeoutExpired as e:
                # result = str(e)
                # print("e:", e)
                # print(e.output)
                result = str(e.output)
                if "New, TLSv1.3," in result:
                    tls_3_in = True
                    break
                if count > 1:
                    break
                else:
                    count += 1
            except subprocess.CalledProcessError:
                if count > 1:
                    break
                else:
                    count += 1
        if tls_3_in:
            return True
        else:
            if result != "":
                if "New, TLSv1.3," in result:
                    return True
                else: return False
            else:
                return False

    def tls_versions(self, url):
        # TODO for spacejam, auditoryneuroscience.com figure out timeout issue, 16 seconds not enough, either false
        # TODO or use openssl on all 4
        # try:
        #     result = subprocess.check_output(["nmap", "--script", "ssl-enum-ciphers", "-p", "443", url],
        #                                     timeout=5).decode("utf-8")
        # except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        #
        #     return None
        args = ["nmap", "--script", "ssl-enum-ciphers", "-p", "443", url]
        result = self.subprocess_caller(args, 10)
        if result != "":
            tls_vers = ["TLSv1.0", "TLSv1.1", "TLSv1.2"]
            return_arr = []
            if result != "":
                for tls in tls_vers:
                    result = self.tls_nmap_helper(result, return_arr, tls)

            tls3 = self.tls_1_3_helper(url)
            if tls3:
                return_arr.append("TLSv1.3")

            if return_arr:
                return return_arr
            else:
                return []
        else:
            return []

    def root_ca(self, url):
        input_url = url + ":443"
        # TODO if it just hangs without timing out try adding shell=True
        count = 0
        return_none = False
        while True:
            try:
                result = subprocess.check_output(["openssl", "s_client", "-connect", input_url], input="",
                                                 stderr=subprocess.STDOUT,
                                                 timeout=timeout_num).decode("utf-8")
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                # result = str(e)
                print("e:", e)
                if count > 1:
                    print("failed thrice root_Ca, url: ", url)
                # print(e.output)
                    return_none = True
                    break
                else:
                    count += 1
                    continue
            break


        if return_none:
            return None
        # print("result: \n", result)
        root_ca = False
        split_result = result.split("O = ")
        if len(split_result) > 1:
            del split_result[0]
            root_ca_split1 = split_result[0].split("CN = ")
            root_ca_split = root_ca_split1[0].split("OU = ")
            root_ca_first = root_ca_split[0]
            index_of_last_comma = root_ca_first.rfind(",")
            root_ca = root_ca_first[:index_of_last_comma]
            # print("Root CA: ", root_ca)
        print("root_ca: ", root_ca)
        if root_ca:
            return root_ca
        else:
            return None

    def rdns_names(self, url):
        ip4_addys = self.scan_output_dictonary["ipv4_addresses"]
        rdns_names_arr = []
        for addy in ip4_addys:
            args = ["nslookup", "-type=PTR", addy]
            result = self.subprocess_caller(args, timeout_num)
            if result != "":
                split_result = result.split("name = ")
                if len(split_result) > 1:
                    del split_result[0]
                    name_split = split_result[0].split("\n\n")
                    name = name_split[0]
                    if name[-1] == ".":
                        name = name[:-1]
                        rdns_names_arr.append(name)
        if rdns_names_arr:
            return rdns_names_arr
        else:

            return []

    def rtt_range(self, url):
        ranges = []
        min_max_tuple = []
        ip4_addys = self.scan_output_dictonary["ipv4_addresses"]
        # print(ip4_addys[0])
        for addy in ip4_addys:
            ip_string = "time echo -e '\x1dclose\x0d' | telnet " + str(addy) + " 443"

            count = 0
            return_none = False
            while True:
                try:
                    result = subprocess.check_output(["sh", "-c", ip_string],
                                                     timeout=timeout_num, stderr=subprocess.STDOUT).decode("utf-8")
                    break
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                    print("e:", e)
                    if count > 1:
                        # This particular IP address's rtt won't be in the domain's rtt_range.
                        print("failed thrice rtt_range, ipv4 address: ", addy)
                        return_none = True
                        break
                    else:
                        count += 1
            if return_none:
                continue

            result_arr = result.split("real\t")
            del result_arr[0]
            num_arr = result_arr[0].split("s")
            num_time = num_arr[0].split("m")
            rtt = int((int(num_time[0]) * 60 * 1000) + (float(num_time[1]) * 1000))
            ranges.append(rtt)

        if len(ranges) == 0:
            return [-1, -1]
        min_max_tuple = [min(ranges), max(ranges)]
        return min_max_tuple

    def geo_locations(self, url):
        ip4_addys = self.scan_output_dictonary["ipv4_addresses"]
        locations = []

        reader = maxminddb.open_database('GeoLite2-City.mmdb')
        for addy in ip4_addys:
            loc_data = reader.get(addy)
            location = ""
            location_keys = loc_data.keys()

            if 'city' in location_keys:
                location += loc_data['city']['names']['en'] + ", "
            if 'subdivisions' in location_keys:
                location += loc_data['subdivisions'][0]['names']['en'] + ", "
            if 'country' in location_keys:
                location += loc_data['country']['names']['en']
            if location == "":
                if 'continent' in location_keys:
                    location = loc_data['continent']['names']['en']
            # print(location)
            locations.append(location)

        reader.close()
        locations = list(dict.fromkeys(locations))

        return locations



s = ScanClass(input_file, output_file)
