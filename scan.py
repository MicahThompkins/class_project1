import json
import sys
import time

command_input = sys.stdin.readline()
input_file, output_file = command_input.split(" ")



def main(input_file, output_file):
    file = open(input_file, 'r')
    file_lines = file.readlines()
    for line in file_lines:
        output = scan(line)

def scan(url):
    output = scan_time()
    return output

def scan_time():
    return time.time()