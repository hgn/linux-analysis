#!/usr/bin/env python3

import os
import pathlib
import elftools
import subprocess
from collections import defaultdict


from elftools.elf.elffile import ELFFile


def get_paths():
    path_raw = os.getenv('PATH').split(':')
    return [pathlib.Path(i) for i in path_raw]

def path_objects():
    all_objects = []
    for path in get_paths():
        for file in path.iterdir():
            if not file.is_file():
                continue
            all_objects.append(file)
    return all_objects

def find_deps(filename):
    deps = []
    with open(filename, 'rb') as fd:
        try:
            elf = elftools.elf.elffile.ELFFile(fd)
        except elftools.common.exceptions.ELFError:
            print(f'{filename}LIB NO ELF')
            return []
        for section in elf.iter_sections():
            if not isinstance(section, elftools.elf.dynamic.DynamicSection):
                continue
            runpath = None
            for tag in section.iter_tags():
                if not hasattr(tag, "runpath"):
                    continue
                runpath = pathlib.Path(tag.runpath)
            for tag in section.iter_tags():
                if not hasattr(tag, "needed"):
                    continue
                full_path = find_library(tag.needed, runpath)
                deps.append(full_path)
        return deps

def iter_files(path):
    for file_or_directory in path.rglob("*"):
        if file_or_directory.is_file():
            yield file_or_directory

def find_library(name, rpath):
    if rpath:
        paths = [rpath]
    else:
        paths = []
    paths.extend([pathlib.Path('/lib'), pathlib.Path('/usr/lib'), pathlib.Path('/lib64'), pathlib.Path('/usr/lib64'), pathlib.Path('/usr/local/lib/')])
    for path in paths:
        for my_file in iter_files(path):
            if str(my_file).endswith(name):
                return my_file
    return None

def main_probeable(filename):
    command = f"perf probe --funcs -x {filename}"
    try:
        out = subprocess.check_output(command.split(), universal_newlines=True)
    except subprocess.CalledProcessError:
        return False
    if 'main' in out.splitlines():
        return True
    else:
        return False

def main():
    # autovivication in py 
    di = defaultdict(int)

    for filename in path_objects():
        di["all"] += 1
        with open(filename, 'rb') as fd:
            try:
                elf = elftools.elf.elffile.ELFFile(fd)
            except elftools.common.exceptions.ELFError:
                print(f'{filename} - no ELF file, skipping')
                continue
            di["valid_elf"] += 1
            if not elf.header.e_type in ["ET_DYN", "ET_EXEC"]:
                continue
            print(f'{filename}')
            ret = main_probeable(filename)
            if ret:
                print(f' main IS traceable')
                di["has_traceable_main"] += 1
            else:
                print(f' main IS NOT traceable')
                di["has_no_traceable_main"] += 1
            for section in elf.iter_sections():
                if not isinstance(section, elftools.elf.dynamic.DynamicSection):
                    continue
                #print(f'  section: {section}')
                runpath = None
                for tag in section.iter_tags():
                    if not hasattr(tag, "runpath"):
                        continue
                    runpath = pathlib.Path(tag.runpath)
                for tag in section.iter_tags():
                    if not hasattr(tag, "needed"):
                        continue
                    #full_path = find_library(tag.needed, runpath)
                    #print(f'  {full_path}')
                    #deps = find_deps(full_path)
                    #for dep in deps:
                    #    print(f'    {dep}')



    print(di)


if __name__ == "__main__":
    main()
