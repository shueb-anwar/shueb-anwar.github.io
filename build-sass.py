#!/usr/bin/env python
#
# No Rights Reserved
# http://creativecommons.org/publicdomain/zero/1.0/
"""Build Bootstrap from SCSS sources with Python

Install Bootstrap::

    bower install bootstrap

Install Python dependencies::

    pip install libsass

Add customized files::

    ./bower_components/
    ./scss/
        bootstrap.scss
        _variables.scss

Run::

   python build-bootstrap.py
"""
import os
import shutil
import logging
import sass

BASE_DIR = os.path.realpath(os.path.dirname(__file__))

LIBS_SRC = [
    './static/sass/style.scss',
]

LIBS_DST = os.path.join(BASE_DIR, 'static', 'css')


# Console util >>>

def console_output():
    console = logging.getLogger('console')
    console.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    console.addHandler(ch)

    def echo(message, *args):
        more = ' '.join(map(str, args)) if args else ''
        console.info(message + more)

    return echo

echo = console_output()

# <<< Console util


def build_scss(filename):
    name, ext = os.path.splitext(filename)
    newname = name + '.css'
    with open(newname, 'w') as css:
        css.write(sass.compile(filename=filename))
    return newname


def proc_file(filename):
    name, ext = os.path.splitext(filename)
    if ext == '.scss':
        filename = build_scss(filename)
    return filename


def copy_file(filename, dst_dir):
    path_src = os.path.join(BASE_DIR, filename)
    path_dst = os.path.join(dst_dir, os.path.basename(filename))

    current_dir = os.getcwd()
    echo("%s -> %s" % (
        path_src.replace(current_dir, '.'),
        path_dst.replace(current_dir, '.')))

    if not os.path.exists(path_dst) or (
        os.path.getctime(path_src) > os.path.getctime(path_dst)):
            shutil.copy2(path_src, path_dst)


def build_lib_files():
    echo("Building lib files:")
    for filename in LIBS_SRC:
        copy_file(proc_file(filename), LIBS_DST)


if __name__ == '__main__':
    build_lib_files()
