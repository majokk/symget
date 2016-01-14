#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv, exit
import symget_basefunctions
import datetime, re

sym_map=symget_basefunctions.sym_map

help = """
    \t"-map"\t\tprint character map 
    \t"-a"\t\tappend (format: "-a keyword symbol")
    \t"-h","-help"\tprint this help message
    \t"-s"\t\tsubstitutes ^keywords^ in a phrase with symbols
    \t"-r"\t\ttakes a keyword as argument and removes \"key\" \"symbol\" pair from map

    \tAll other arguments are interpreted as keyword calls.\n
    \tFor substitution, there may be command line erros if
    \tthe phrase is not enclosed in quotation marks\n"""

timestamp=datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

def get_from_map_super(keyword=argv[1:]):

    symbols = symget_basefunctions.get_from_map_base(keyword)
    clean_symbols = [item for item in symbols if item != "None"]

    if clean_symbols != []: # check whether any symbol has been retrieved from map
        print "Symbols: {}".format(" ".join(clean_symbols)) # if yes, prints them out
    else:
        pass 

    symget_basefunctions.put_to_clipboard(" ".join(clean_symbols))
    symget_basefunctions.log_last_call(clean_symbols)

    return symbols

def append_map_super():

    # checks input format
    try:
        new_keyword,new_symbol = argv[2], argv[3]
    except IndexError:
        print "\nKeyword and/or symbol missing, try again"
        print help
        exit(0)

    # appends or rejects if keywords clash
    if symget_basefunctions.keyword_clash(new_keyword) == True:
        old_symbol = symget_basefunctions.get_from_map_base([new_keyword])[0]
        old_keyword = new_keyword
        
        print "\n\tSuggested keyword already exists."
        print "\tExisting pair in character map:  '%s':'%s'\n" % (old_keyword, old_symbol)
        
    else:
        symget_basefunctions.append_map_base(new_keyword, new_symbol)
        print "Charater map successfully appended with \"{}\" \"{}\" pair".format(new_keyword,new_symbol)
        
def substitute_phrase():
    
    phrase = " ".join(argv[2:])

    replace_keys_raw = re.findall(r"\^.*?\^", phrase) # regexes keywords from cml argumend
    replace_keys_stripped = [item.strip("^") for item in replace_keys_raw] # strips keyword markers (^^)
    symbols = get_from_map_super(replace_keys_stripped) # gets symbols from map

    summarized = zip(replace_keys_raw, replace_keys_stripped, symbols) # creates a list of 3-tuples
    
    for item in summarized: # do the substituion
        if item[2] != "None": # if the symbol was not found, leave the keywod in the output string
            phrase = phrase.replace(item[0], item[2])
        else:
            continue

    if replace_keys_raw != []:
        print "Subsituted phrase: {}".format(phrase)
    else:
        print "No keywords subsituted."  
    
    symget_basefunctions.put_to_clipboard(phrase)

def print_map():
    # determines column length according to nr of items in map and prints formatted map

    col1 = []
    col2 = []
    col3 = []

    total_len = sum(1 for item in symget_basefunctions.file_reader(sym_map)) # total num of items in file

    # if not divisible by three, then +1 to col length
    if total_len % 3 == 0:
        col_len = total_len/3
    else:
        col_len = (total_len/3)+1

    # fill column lists from by column length
    for num,item in enumerate(symget_basefunctions.file_reader(sym_map)):
        if num+1 <= col_len:
            col1.append(item)
        elif col_len < num+1 <= col_len*2:
            col2.append(item)
        elif col_len*2 < num+1 <= col_len*3:
            col3.append(item)
        else:
            raise IndexError
            exit(0)

    # filler for last column, zip requires equal length lists to display properly
    for num in range(len(col1)-len(col3)):
        col3.append("")

    columnified = zip(col1, col2, col3)

    # num for troubleshooting if not displaying correctly, probably not necessary
    for num,args in enumerate(columnified):
        print "{:<4}{:20}\t{:20}\t{:20}".format(num+1,*args)

def remove_pair():

    try:
        delkey = argv[2]
        for line in symget_basefunctions.file_reader(sym_map):
            if delkey == line.split(",")[0]:
                break
            else:
                continue
        else:
            print "Keyword not found in map"
            exit(0)

        print "Press enter to to delete \"{}\" from character map or ctrl-D to cancel.".format(delkey)
        raw_input(": ")

        symget_basefunctions.backup_map()

        # a generator expression that returns a tuple of items from generator file_reader
        # ... which returns lines sym_map
        key_value = ((line.split(",")[0],line.split(",")[1]) for line in symget_basefunctions.file_reader(sym_map))
        map_cache = dict(key_value)

        with open(sym_map, "w") as target:
            for key,value in map_cache.iteritems():
                if delkey != key:
                    target.write(key+","+value+"\n")
                else:
                    continue

        print "{} deleted from sym_map".format(delkey)

    except EOFError:
        exit(0)


def program_starts_here():
    try:
        if argv[1] == "-a":
            append_map_super()
        elif argv[1] == "-s":
            substitute_phrase()
        elif argv[1] == ("-h" or "help" or "help"):
            print help
        elif argv[1] == "-map":
            print_map()
        elif argv[1] == "-r":
            remove_pair()
        else:
            get_from_map_super()
    except IndexError:
        print help


program_starts_here()
