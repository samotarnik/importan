import glob
import os
import sys
import pprint

from src.pyfile import Pyfile
from src.parser import Parser


def get_working_directory():
    if not len(sys.argv) == 2:
        raise Exception('pass a folder to inspect as an argument')
    path = os.path.abspath(sys.argv[1])
    if not os.path.isdir(path):
        raise ValueError('argument {} is not a folder'.format(sys.argv[1]))
    return path


def find_all_py_files_in(folder):
    file_names = glob.glob(folder + '/**/*.py', recursive=True)
    return [Pyfile(file_name, folder) for file_name in file_names]

def longest_common_prefix(y, xs):
    return max([os.path.commonprefix([x, y]) for x in xs], key=len).rstrip('.')


def main():
    working_dir = get_working_directory()
    py_files = find_all_py_files_in(working_dir)

    ex = {f.module: Parser(f.module, f.lines()).extract() for f in py_files if not f.module.startswith('tests')}
    modules = list(ex.keys())

    # "ROUNDED" GRAPH
    discards = set([])
    for module, imports in ex.items():
        cleaned = set([])
        for imp in imports:
            if imp in modules:
                cleaned.add(imp)
            else:
                pre = longest_common_prefix(imp, modules)
                if pre and pre not in modules:
                    pre = pre + '.__init__'
                if pre not in modules:
                    discards.add(imp)
                else:
                    cleaned.add(pre)
        ex[module] = cleaned

    with open('asdf.gv', 'w') as f:
        f.write('digraph {\n')
        for module, imports in ex.items():
            for imp in imports:
                f.write('    "{}" -> "{}";\n'.format(module, imp))
        f.write('}\n')

    pprint.pprint(discards)


if __name__ == '__main__':
    main()

