import os
from os.path import join, expanduser
import json
import shutil


ROOT = join(expanduser("~"), "polarishub")

def make_dir(path):
    # print(path)
    if os.path.exists(path):
        print("Directory already exists!")
        return False
    else:
        os.mkdir(path)
        print("Making directory successes!")
        return True

def choose_file_dir(path):
    if os.path.exists(path):
        print("Directory already exists! Used as the file directory.\nYou may check for unsharable files.")
        # return False
    else:
        os.mkdir(path)
        print("New directory.\nYou can copy and paste your shared files to it.")
        # return True

def init_files(path):
    settings = {
        'path': input("Please input your file directory (Do not use the User Directory!) :")
    }

    choose_file_dir(settings['path'])
    
    settings['admin-password'] = input("Please input your admin password:")
    settings['username'] = input("Please input your username:")
    json.dump(settings, open(join(path, 'settings.json'), 'w'))
    print("Settings saved.\n"+'-'*50+"\n")

    passwords = {}
    json.dump(passwords, open(join(path, 'passwords.json'), 'w'))
    print("Passwords initialized.\n"+'-'*50+'\n')

    print("Setup finished!")

if not make_dir(ROOT):
    while True:
        clear = input("Do you want to reset your all settings(Y/N)?")
        if clear == "Y" or clear == 'y':
            shutil.rmtree(ROOT)
            os.mkdir(ROOT)
            break
        elif clear == "N" or clear == 'n':
            break
        else:
            print("Please Enter Y / N !")

init_files(ROOT)
input("Enter to exit.")