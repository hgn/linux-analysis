#!/usr/bin/env python3

import os
import pathlib
import elftools
import subprocess
import rich

from types import SimpleNamespace
from collections import defaultdict
from collections import OrderedDict
from elftools.elf.elffile import ELFFile

# and libraries
class Executable(object):

    def __init__(self, filename):
        self.filename = filename
        self.is_elf = None
        self.is_executable = False
        self.is_main_probeable = False
        self.libraries = OrderedDict()
        self.stat = SimpleNamespace()
        self.stat.file_size = None
        self.stat.has_dwarf = False

    def _print_libraries_graph(self, nesting=4):
        for name, lib in self.libraries.items():
            pre_space = nesting * " "
            print(f'{pre_space}{lib.filename} [filesize: {self.stat.file_size} byte]')
            lib._print_libraries_graph(nesting+4)

    def _get_all_libs_recursive(self):
        libs_flat = set()
        for name, lib in self.libraries.items():
            libs_flat.add(lib.filename)
            libs_flat.update(lib._get_all_libs_recursive())
        return libs_flat

    def _print_libraries_flat(self):
        libs = self._get_all_libs_recursive()
        for lib in libs:
            print('  {}'.format(lib))

    def print_libraries(self, mode='flat'):
        if mode == 'flat':
            self._print_libraries_flat()
        else:
            self._print_libraries_graph()

    def print_intro(self):
        if not self.is_elf:
            rich.print(f'[brown]{self.filename} - not ELF file :thumbs_down:[/brown]')
            return
        if not self.is_main_probeable:
            rich.print(f'[yellow]{self.filename} - function main not probeable[/yellow]')
            return
        rich.print(f'[green]{self.filename} - function main probeable[/green]')

    def calc_stats(self):
        self.stat.file_size = 0
        self.stat.file_size = self.filename.stat().st_size
        # and recursivly
        for name, lib in self.libraries.items():
            lib.calc_stats()

    def print_stats(self):
        pass

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

def find_library(name, rpath):
    if rpath:
        paths = [rpath]
    else:
        paths = []
    paths.extend([pathlib.Path('/lib/x86_64-linux-gnu'),
                  pathlib.Path('/lib'),
                  pathlib.Path('/usr/lib/x86_64-linux-gnu/'),
                  pathlib.Path('/usr/lib'),
                  pathlib.Path('/lib64'),
                  pathlib.Path('/usr/lib64'),
                  pathlib.Path('/usr/local/lib/'),
                  pathlib.Path('/usr/lib/jvm/java-11-openjdk-amd64/lib/jli/'),
                  pathlib.Path('/usr/lib/x86_64-linux-gnu/darktable/'),
                  pathlib.Path('/usr/lib/x86_64-linux-gnu/systemd/')])
    for path in paths:
        full_path = path / name
        if full_path.is_file():
            return full_path
        #return my_file
    return None

def main_probeable(executable):
    filename = executable.filename
    command = f"perf probe --funcs -x {filename}"
    try:
        out = subprocess.check_output(command.split(), universal_newlines=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        return False
    if 'main' in out.splitlines():
        return True
    else:
        return False

def populate_libraries(executable):
    fd = open(executable.filename, 'rb')
    elf = elftools.elf.elffile.ELFFile(fd)
    for section in elf.iter_sections():
        if not isinstance(section, elftools.elf.dynamic.DynamicSection):
            continue
        executable.runpath = None
        for tag in section.iter_tags():
            if not hasattr(tag, "runpath"):
                continue
            executable.runpath = pathlib.Path(tag.runpath)
        for tag in section.iter_tags():
            if not hasattr(tag, "needed"):
                continue
            full_path = find_library(tag.needed, executable.runpath)
            if not full_path:
                print(f"Cannot find library: {tag.needed}!")
                continue
            dependency = Executable(full_path)
            populate_libraries(dependency)
            executable.libraries[tag.needed] = dependency
    fd.close()


def main():
    stats = defaultdict(int)
    db = OrderedDict()

    for filename in path_objects():
        stats["files"] += 1
        exe = Executable(filename)
        with open(filename, 'rb') as fd:
            try:
                elf = elftools.elf.elffile.ELFFile(fd)
            except elftools.common.exceptions.ELFError:
                exe.is_elf = False
                db[filename] = exe
                stats["non-elf"] += 1
                continue
            if not elf.header.e_type in ["ET_DYN", "ET_EXEC"]:
                exe.is_elf = False
                db[filename] = exe
                stats["non-exec"] += 1
                continue
            if exe.has_dwarf_info():
                exe.stat.has_dwarf = True
            exe.is_elf = True
            exe.is_executable = True
            db[filename] = exe
            stats["exec"] += 1

    rich.print('[yellow]Files in PATH:      {}[/yellow]'.format(stats["files"]))
    rich.print('[yellow]Non-ELF files:      {}[/yellow]'.format(stats["non-elf"]))
    rich.print('[yellow]ELF-Non-Exec files: {}[/yellow]'.format(stats["non-exec"]))
    rich.print('[yellow]ELF-Exec files:     {}[/yellow]'.format(stats["exec"]))

    for filename, executable in db.items():
        if not executable.is_elf:
            continue
        if main_probeable(executable):
            executable.is_main_probeable = True
        populate_libraries(executable)

        executable.print_intro()
        executable.calc_stats()
        executable.print_libraries(mode='flat')


if __name__ == "__main__":
    main()
