#!/usr/bin/env python3

import os
from shutil import rmtree
import sys
import argparse
import magic
import codecs
import json

from joblib import Parallel, delayed
import multiprocessing

def get_download_path():
    home_path = os.path.expanduser('~')
    download_path = home_path + '/Downloads'
    return download_path

def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=('Optimal options'))
    parser.add_argument('-r', '--directory', default=get_download_path(), help='Use your location')
    parser.add_argument('-o', '--output', dest='output', action='store_true', help='A JSON File dumbed')
    options = parser.parse_args(args)
    return options
    

def folder_json(directory,output):
    
    os.chdir(directory)
    ignore_list = ['output.json', 'folder', 'application', 'audio', 'example', 'font', 'image', 'model', 'text', 'video']
    dir = {}

    for ll in os.listdir():
        if(ll not in ignore_list):
            if(os.path.isdir(ll)):
                if('folder' not in dir):
                    dir['folder'] = []
                dir['folder'].append(ll)
            elif(os.path.isfile(ll)):
                type_dir, type_subdir = mime.from_file(ll).split('/')
                if(type_dir not in dir):
                    dir[type_dir] = {}
                if(type_subdir not in dir[type_dir]):
                    dir[type_dir][type_subdir] = []
                dir[type_dir][type_subdir].append(ll)

    if(output):
        with codecs.open('output.json', 'w+', encoding='utf8') as fp:
            json.dump(dir, fp, indent=4, ensure_ascii=False, sort_keys=True)
    
    return dir

'''
def init_workspace(dir, source_folder):
    for x,y in dir.items():
        new_dir = source_folder + '/' + x
        if(not os.path.exists(new_dir)):
            os.mkdir(new_dir)
        if(isinstance(y,dict)):
            for xx in y.keys():
                new_sub_dir = new_dir + '/' + xx
                if(not os.path.exists(new_sub_dir)):
                    os.mkdir(new_sub_dir)
'''

def init_folder(x,y,source_folder):
    new_dir = source_folder + '/' + x
    if(not os.path.exists(new_dir)):
        os.mkdir(new_dir)
    if(isinstance(y,dict)):
        for xx in y.keys():
            new_sub_dir = new_dir + '/' + xx
            if(not os.path.exists(new_sub_dir)):
                os.mkdir(new_sub_dir)

def parallel_init_workspace(dir,source_folder):
    Parallel(n_jobs=multiprocessing.cpu_count())(delayed(init_folder)(x,y,source_folder) for x,y in dir.items())

'''
def manipulate_files(dir, source_folder):
        for x,y in dir.items():
            dest_folder = source_folder + '/' + x
            if(isinstance(y,dict)):
                for xx, xy in y.items():
                    for yy in xy:
                        dest_file = dest_folder + '/' + xx + '/' + yy
                        src_file = source_folder + '/' + yy
                        os.rename(src_file,dest_file)
            else:
                for yy in y:
                    dest_file = dest_folder + '/' + yy
                    src_file = source_folder + '/' + yy
                    if(os.path.exists(dest_file)):
                        rmtree(dest_file)
                    os.rename(src_file,dest_file)
'''

def manipulate_file(x,y,source_folder):
    dest_folder = source_folder + '/' + x
    if(isinstance(y,dict)):
        for xx, xy in y.items():
            for yy in xy:
                dest_file = dest_folder + '/' + xx + '/' + yy
                src_file = source_folder + '/' + yy
                os.rename(src_file,dest_file)
    else:
        for yy in y:
            dest_file = dest_folder + '/' + yy
            src_file = source_folder + '/' + yy
            if(os.path.exists(dest_file)):
                rmtree(dest_file)
            os.rename(src_file,dest_file)

def parallel_manipulate_files(dir, source_folder):
    Parallel(n_jobs=multiprocessing.cpu_count())(delayed(manipulate_file)(x,y,source_folder) for x,y in dir.items())


if __name__ == '__main__':
    
    mime = magic.Magic(mime=True)
    options = get_options()

    folder_tree = folder_json(options.directory, options.output)
    parallel_init_workspace(folder_tree,options.directory)

    parallel_manipulate_files(folder_tree,options.directory)

