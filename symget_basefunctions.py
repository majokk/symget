#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, exit
import csv, datetime, subprocess
import pygtk, gtk
pygtk.require('2.0')

call_log = # path to call log file
sym_map = # path to symbol map
timestamp=datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')


def file_reader(data_file):
    with open(data_file, "rb") as data_file:
        for line in data_file:
            yield line.rstrip('\r\n')

def file_writer(data_file, data, mode):

    with open(data_file, mode) as data_file:
        if isinstance(data,list):
            for item in data:
                data_file.write(item+"\n")
        elif isinstance(data,str):
            data_file.write(data+"\n")
        else:
            raise TypeError

def get_from_map_base(keywords):

    symbols = []

    for key in keywords:
        for line in file_reader(sym_map):
            if line.split(",")[0] == key:
                symbols.append(line.split(",")[1])
                break
        else:
            print "Keyword \"{}\" not found in sym_map.".format(key)
            symbols.append("None") # None appended for use in substitute_phrase()


    return symbols


def append_map_base(key,value):
    backup_map()
    with open(sym_map, "ab") as the_map:
        appender = csv.writer(the_map)
        appender.writerow([key,value])

def keyword_clash(new_keyword):

    for line in file_reader(sym_map):
        map_keyword = line.split(",")[0]
        if new_keyword == map_keyword:
            return True            
    else:
        
        return False

def backup_map():

    backup_map.timestamp=datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    subprocess.call("cp /home/markku/scripts/symget/sym_map /home/markku/scripts/symget/logs/map_logs/"+timestamp, shell=True)

def log_last_call(raw_replacement_list):

    log_list = []
    for item in raw_replacement_list:
        log_list.append("%s %s" % (item, timestamp))

    file_writer(call_log, log_list, "a")

def put_to_clipboard(text):

    if isinstance(text,list):
        text = " ".join(text)
    elif isinstance(text,str):
        pass
    else:
        raise TypeError

    clipboard = gtk.clipboard_get()
    clipboard.set_text(text)
    clipboard.store()
