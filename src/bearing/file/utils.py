# -*- coding: utf-8 -*-
"""Provides File Utils."""
import os
import pathlib
import shutil
import ntpath
from collections import defaultdict


def delete_contents(folder):
    """Empty DIR of all files."""
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


def etree_to_dict(t):
    """Return a tree as a DICT."""
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(("@" + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]["#text"] = text
        else:
            d[t.tag] = text
    return d


def create_dir(dir_path):
    """Create, if not exists, DIR."""
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    else:
        pass


def list_dirs(rootdir):
    """List directories in DIR."""
    dirs = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            dirs.append(file)
    return dirs


def copy_file(src, dst):
    """Copy file from src-path to destination-path."""
    shutil.copyfile(src, dst)


def list_files(rootdir, ext=None):
    """List the files in DIR, ext=optional."""
    files = os.listdir(rootdir)
    files = [f for f in files if os.path.isfile(os.path.join(rootdir, f))]
    if ext:
        files = [f for f in files if ext == pathlib.Path(f).suffix]
    return files


def copy_files(source_dir, target_dir):
    """Copy files from source to target."""
    file_names = os.listdir(source_dir)
    for file_name in file_names:
        # shutil.move(os.path.join(source_dir, file_name), target_dir)
        source = os.path.join(source_dir, file_name)
        target = os.path.join(target_dir, file_name)
        shutil.copyfile(source, target)


def path_leaf(path):
    """Return the leaf of path."""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
