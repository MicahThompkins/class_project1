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
        json.dump(output_dictonary, f, sort_keys=True, indent=4)
        f.close()


def scan(url):
    output_dictonary = {}
    scan_time_output = scan_time()
    output_dictonary["scan_time"] = scan_time_output
    return output_dictonary

def scan_time():
    return time.time()

main(input_file, output_file)