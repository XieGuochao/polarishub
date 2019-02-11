from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, Http404, HttpResponseServerError
import os
from os.path import join, expanduser
import json
import socket

ROOT = join(expanduser("~"), "polarishub")

def loadSettings():
    global settings, FILEROOT
    try:
        settings = json.load(open(join(ROOT, 'settings.json'), 'r'))
        FILEROOT = settings['path']
    except:
        settings = None
        FILEROOT = None
    print("load settings success")
    return settings

def loadPasswords():
    global passwords
    try:
        passwords = json.load(open(join(ROOT, 'passwords.json'), 'r'))
    except:
        passwords = None
    print("load passwords success")
    return passwords

def loadFileList():
    global fileList
    fileList = list(os.walk(FILEROOT))[0][2]
    return fileList

def saveSettings():
    json.dump(settings, open(join(ROOT, 'settings.json'), 'w'))

def savePasswords():
    json.dump(passwords, open(join(ROOT, 'passwords.json'), 'w'))

def listFileList():
    loadFileList()
    print('\n'.join(fileList))
    print("-"*50+"\n")
    
def getIP():
    return socket.gethostbyname(socket.gethostname())

def checkAdminPassword(password):
    return password == settings['admin-password']

def changeSettings(key, value, password="null", requirePassword=True):

    if checkAdminPassword(password) or not requirePassword:
        settings[key] = value
        saveSettings()
        loadSettings()
        print("Change settings success")
        return True
    else:
        print("Invalid admin password.")
        return False

def changePasswords(key, value, password="null", requirePassword=True):
    if checkAdminPassword(password) or (not requirePassword):

        if key not in fileList:
            return "No File"
        if value is None or value == "null" or value == '':
            del passwords[key]
        else:
            passwords[key] = value
        savePasswords()
        loadPasswords()
        print("Success")
        return True
    else:
        print("Invalid admin password.")
        return False


def changeAdminPassword(old_password, new_password):
    if checkAdminPassword(old_password):
        settings['admin-password'] = new_password
        saveSettings()
        return True
    else:
        print("Invalid admin password.")
        return False


loadSettings()
loadPasswords()
loadFileList()