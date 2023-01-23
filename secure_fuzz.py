#!/usr/bin/env python3 
import os
import sys, getopt
from simple_term_menu import TerminalMenu
from pwn import *
import signal, threading, re
import time

import subprocess as sp

from argparse import ArgumentParser

#python3 secure_fuzz.py -u https://www.test.com/FUZZ -e .htmp,.php -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt

##################Ctrl+C

def def_handler(sig, frame):
    print("\n[!] Exiting...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

###############################



## Global Variables
url = "https://prod.logista.plus.movilizer.com/ui/FUZZ"
output_name = sp.getoutput("echo %s | sed 's/https\:\/\///g' | sed 's/\/FUZZ//g' | sed 's/\./_/g' | sed 's/_$//g' | sed 's/\//_/g' | xargs"%(url))
current_folder = sp.getoutput("pwd")
threads = 1
#ext=".asp,.aspx"->Don't add spaces!!
extensions = ""
step = 1000
start = 1
finish = start+step


#def prepare_environment():

 
 
def list_files(directory):
    return (file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file)))
 
 
def which_wordlist(directory):
    options = [option for option in list_files(directory)]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    file_route_path = f"{directory}/{options[menu_entry_index]}"
    return(f"{file_route_path}")
 

def prepare_systemfile(directory):
    #print("The directory of the wordlist is %s"%(directory))
    p1 = log.progress("Preparing environment...")
    p1.status("Creating folders neccesary:")
    time.sleep(2)
    wordlist_local_name = sp.getoutput("echo '%s' | awk '{print $NF}' FS='/' | awk '{print $1}' FS='.'"%(directory))
    output_local_folder = "output/" + output_name
    wordlist_local_name = "wordlists/wordlist_" + output_name + "_" + wordlist_local_name
    p1.status("The name of the wordlist chosen is %s"%(wordlist_local_name))
    
    p2 = log.progress("Creating Folders..")
    p2.status("Folder to save the subdictionaries...")
    time.sleep(2)

    #check if the wordlist folder exists already
    isExist = os.path.exists(wordlist_local_name)

    if not isExist:
        wordlist_local_name_path = wordlist_local_name
        os.system("mkdir -p %s"%(wordlist_local_name_path))
        p2.success("The folder was created!")
        p3 = log.progress("Spliting...")
        p3.status("Spliting the wordlist into the folder...")

        time.sleep(2)
        os.system("split -l %s %s ./%s/segment_"%(step,directory,wordlist_local_name_path))
        p3.success("Wordlist splited!")
        time.sleep(2)

    #if the wordlist folder exist dont create nothing and jump to the next instruction, resume the fuzzing
    else:
        p2.success("The folder already exists. Let's resumen the fuzzing!")
    p1.success("Environment created!")


    #The output folder
    os.system("mkdir -p %s"%(output_local_folder))


    return wordlist_local_name, output_local_folder

def menu(argv):
    help = 'secure_fuzz.py -u https://test.com/FUZZ -t 1 -e .php,.aspx,.config --step 1000'
    url = ''
    extensions = ''
    threads = 1
    steps = 1000
    wordlist = "/usr/share/seclists/Discovery/Web-Content"
    

    parser = ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="https://test.com/FUZZ")
    parser.add_argument("-e", "--extensions", dest="extensions", help=".html,.php")
    parser.add_argument("-t", "--threads", dest="threads", help="default 1")
    parser.add_argument("-s", "--steps", dest="steps", help="size for each subwordlist, default 1000")
    parser.add_argument("-w", "--wordlist", dest="wordlist", help="Path for the big wordlist, may be a folder or a file")

    args = parser.parse_args()

    url = args.url
    extensions = args.extensions
    threads = args.threads
    wordlist = args.wordlist
    steps = args.steps
    
    #logs
    '''
    print ('Url: ', url)
    print ('Extensions: ', extensions)
    print ('Threads: ', threads)
    print ('wordlist: ', wordlist)
    print ('steps: ', steps)
    '''

    if url == "":
        print("parameter -u is mandatory!")
        print(help)
        sys.exit(1)
    else:
        return url, extensions, threads, steps, wordlist


def fuzzing(url, extensions, wordlist_local_name, output_local_folder):
    print(url)
    print(extensions)
    print(wordlist_local_name)
    print(output_local_folder)

    extensions_empty = True

    if extensions == "":
        print("Extension Empty")
    else:
        print("Extension NOT Empty!")
        extensions_empty = False
        extensions = "-e " + extensions

    time.sleep(10)

    list_wordlists = sorted(list(list_files(wordlist_local_name)))
    i = 0
    while len(list_wordlists) > 0:
        current_wordlist = list_wordlists[0]
        #os.system("")
        print("ffuf -u %s -w %s/%s %s -o %s.json -of json -rate 5 -H 'User-Agent: custom string'"%(url, wordlist_local_name, current_wordlist, extensions, output_local_folder))
        print(current_wordlist)
        os.system("ffuf -u %s -w %s/%s %s -o %s.json -of json -rate 5 -H 'User-Agent: custom string'"%(url, wordlist_local_name, current_wordlist, extensions, output_local_folder))
        p1 = log.progress("Exiting...")
        p1.success("Press Ctrl+C again to exit the program definitivelly!")
        time.sleep(10)
        os.system("rm %s/%s"%(wordlist_local_name, current_wordlist))
        list_wordlists = sorted(list(list_files(wordlist_local_name)))

    if len(list_wordlists) == 0:
        os.system("rmdir %s"%(wordlist_local_name))


if __name__ == "__main__":

    print("Choose the wordlist to fuzz")
    #time.sleep(2)
    

    url, extensions, threads, steps, wordlist = menu(sys.argv[1:])
    time.sleep(2)


    if os.path.isdir(wordlist):  
        wordlist_directory = wordlist
        wordlist = which_wordlist(wordlist_directory)
    else:
        #Este else creo que no debe tener nada concreto
        #directory = str(sys.argv[1])
        wordlist_directory = "/usr/share/seclists/Discovery/Web-Content"


    #Function to deploy the filesystem for the fuzzing
    wordlist_local_name, output_local_folder = prepare_systemfile(wordlist)

    print("pre-fuzzing")
    fuzzing(url, extensions, wordlist_local_name, output_local_folder)
    print("post-fuzzing")
 
