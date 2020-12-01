import json
import sys
import texttable
from operator import itemgetter

command_input = sys.argv
timeout_num = 1
input_file = str(command_input[1])
output_file = str(command_input[2])

# Parse through data, add rows
with open(input_file) as f:
    data = json.loads(f.read())

tab2 = texttable.Texttable()
tab3 = texttable.Texttable()
tab4 = texttable.Texttable()
tab5 = texttable.Texttable()

categories = ["Domain", "Server Name", "Root Certificate Authority", "TLS Versions", "Locations", "Scan Time", "RTT Range", "Listens for Unencrypted HTTP",
                   "Redirects to HTTPS", "HSTS Enabled", "IPv4 Addresses", "IPv6 Addresses", "Reverse DNS Names"]
names = ["Domain", "http_server", "root_ca", "tls_versions", "geo_locations", "scan_time", "rtt_range", "insecure_http",
                   "redirect_to_https", "hsts", "ipv4_addresses", "ipv6_addresses", "rdns_names"]

# Part 3.1
# Create Table of values from part 2
def one(url):
    tab1 = texttable.Texttable()
    width = [20, 30]
    alignment = ['c', 'c']
    tab1.set_cols_width(width)
    tab1.set_cols_align(alignment)
    tab1.set_cols_dtype(["t", "t"])

    pointer = 0
    tab1.add_rows([[categories[pointer], url]], header=True)
    pointer += 1
    while pointer < 13:
        tab1.add_row([categories[pointer], data[url][names[pointer]]])
        pointer += 1

    return tab1

# Part 3.2
def two():
    tab2.add_rows([["Domain", "Minimum RTT"]], header= True)
    tab2.set_cols_width([27, 13])
    tab2.set_cols_align(['c', 'c'])


    rows = []
    for key in data:
        # RTT RANGE FIX
        if data[key]["rtt_range"] is None:
            tuple = [key, None]
        else:
            tuple = [key, data[key]["rtt_range"][0]]
        rows.append(tuple)
    rows = sorted(rows, key=itemgetter(1))

    for i in range(len(rows)):
        tab2.add_row([rows[i][0], rows[i][1]])

# Part 3.3
def three():
    tab3.add_rows([["Root Certificate Authority", "Number of Occurrences"]], header=True)
    tab3.set_cols_width([20, 15])
    tab3.set_cols_align(['c', 'c'])

    rows_dict = {}

    for key in data:
        if data[key]["root_ca"] in rows_dict:
            rows_dict[data[key]["root_ca"]] = rows_dict.get(data[key]["root_ca"]) + 1
        else:
            rows_dict[data[key]["root_ca"]] = 1
    if None in rows_dict.keys():
        del rows_dict[None]
    rows_dict = dict(sorted(rows_dict.items(), key=lambda item: item[1], reverse=True))

    for key in rows_dict:
        tab3.add_row([key, rows_dict[key]])

# Part 3.4
def four():
    tab4.add_rows([["Server Name", "Number of Occurrences"]], header=True)
    tab4.set_cols_width([25, 15])
    tab4.set_cols_align(['c', 'c'])

    rows_dict = {}

    for key in data:
        if data[key]["http_server"] in rows_dict:
            rows_dict[data[key]["http_server"]] = rows_dict.get(data[key]["http_server"]) + 1
        else:
            rows_dict[data[key]["http_server"]] = 1

    if None in rows_dict.keys():
        del rows_dict[None]
    rows_dict = dict(sorted(rows_dict.items(), key=lambda item: item[1], reverse=True))

    for key in rows_dict:
        tab4.add_row([key, rows_dict[key]])

# Part 3.5
def five():
    tab5.add_rows([["Supported", "Percentage"]], header=True)
    tab5.set_cols_width([15, 15])
    tab5.set_cols_align(['c', 'c'])

    total_num_domains = len(data.keys())
    supporteds = ["TLSv1.0", "TLSv1.1", "TLSv1.2", "TLSv1.3", "Plain HTTP", "HTTP Redirect", "hsts", "IPv6"]
    supporteds_nums = [0] * 8 # tls1.0 tls1.1 tls1.2 tls1.3 e f g c


    for keys in data:
        x = data[keys]

        if x["insecure_http"] == True:
            supporteds_nums[4] += 1
        if x["redirect_to_https"] == True:
            supporteds_nums[5] += 1
        if x["hsts"] == True:
            supporteds_nums[6] += 1
        if len(x["ipv6_addresses"]) > 0:
            supporteds_nums[7] += 1

        # TLS
        tls = x["tls_versions"]
        if tls is None:
            continue

        for version in tls:
            if version == "TLSv1.0":
                supporteds_nums[0] += 1
            elif version == "TLSv1.1":
                supporteds_nums[1] += 1
            elif version == "TLSv1.2":
                supporteds_nums[2] += 1
            elif version == "TLSv1.3":
                supporteds_nums[3] += 1

    tab5.add_rows([["SSLv2", 0], ["SSLv3", 0]], header = False)
    for i in range(8):
        name = supporteds[i]
        perc = supporteds_nums[i]/total_num_domains * 100
        tab5.add_row([name, perc])


# when finished
two()
three()
four()
five()
horizontal_line = "--------------------------------------------------------------------"

with open(output_file, 'w') as f:
    f.write("Tables 3.1: \n")

    for key in data:
        tab = one(key)
        f.write(tab.draw())
        f.write("\n\n\n")

    f.write(horizontal_line)
    f.write("\nTable 3.2: \n")
    f.write(tab2.draw())
    f.write("\n\n\n")

    f.write(horizontal_line)
    f.write("\nTable 3.3: \n")
    f.write(tab3.draw())
    f.write("\n\n\n")

    f.write(horizontal_line)
    f.write("\nTable 3.4: \n")
    f.write(tab4.draw())
    f.write("\n\n\n")

    f.write(horizontal_line)
    f.write("\nTable 3.5: \n")
    f.write(tab5.draw())
    f.write("\n\n\n")

    f.close()
