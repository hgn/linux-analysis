#!/usr/bin/env python3

import subprocess
import re
import sys

def get_text_section_info(binary_path):
    objdump_output = subprocess.check_output(['objdump', '-h', binary_path], universal_newlines=True)

    for line in objdump_output.splitlines():
        if '.text' in line:
            fields = line.split()
            size = int(fields[2], 16)
            start_address = fields[3]
            return start_address, size

    raise Exception(f"Failed to find .text section in {binary_path}")

def disassemble_with_r2(binary_path, start_address, size):
    r2_command = f"aaa; iS; pD {size} @ 0x{start_address}"
    subprocess.run(['r2', '-e', 'bin.relocs.apply=true', '-q', '-c', r2_command, binary_path])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <binary_path>")
        sys.exit(1)

    binary_path = sys.argv[1]

    try:
        start_address, size = get_text_section_info(binary_path)
        disassemble_with_r2(binary_path, start_address, size)

    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

