from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, FileResponse, Http404, HttpResponseServerError
import os
from os.path import join, expanduser
import json
import socket
import api
from serverhub.myqrcode import generateCode
import hashlib

# Create your views here.

ROOT = join(expanduser("~"), "polarishub")
try:
    settings = json.load(open(join(ROOT, 'settings.json'), 'r'))
    FILEROOT = settings['path']
except:
    settings = None
    FILEROOT = None

try:
    passwords = json.load(open(join(ROOT, 'passwords.json'), 'r'))
except:
    passwords = None

def name2md5(files):
    reslist = []
    for file in files:
        m = hashlib.md5()
        m.update(file.encode())
        reslist.append(m.hexdigest())
    return reslist


def getIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    resIP = s.getsockname()[0]
    s.close()
    return resIP

def check(request):
    if settings != None:
        return HttpResponse(json.dumps(settings) + getIP())
    else:
        return HttpResponse("No settings!" + getIP())

def getFiles(request):
    port = request.META.get("SERVER_PORT")
    if FILEROOT!= None:
        files = list(os.walk(FILEROOT))[0][2]
        filesmd5 = name2md5(files)
        htmlpart = "\n".join(["<a href=\"file/"+filesmd5[i]+"\" target=\"_blank\">"+files[i]+"</a> \
            <a href=\"getQR?url=http://" + getIP() + ":" + str(port) +"/file/" + filesmd5[i] + "&filename=qrcode.png\"><button>Share</button></a>\
                <br>" for i in range(len(files))])
        return HttpResponse(
            """<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <title>{}'s PolarisHub</title>
                <meta name="viewport" content="width=device-width, initial-scale=1">
            </head>
            <body>
            <style>
                input, button {{ border-radius: .5rem; background: white; box-shadow: 2px 2px 1px rgba(0,0,0,0.3); height: 2rem; width: fit-content; }}

                input {{width: 15rem; padding-left: 1rem}}
            </style>
                <h1>{}'s Files</h1>
                <h3>{}:{}</h3>
                {}
                {}
            </body>
            </html>""".format(settings['username'], settings['username'], getIP(), port, "<a href='settings'><h3>Settings</h3></a><br>" if checkIP(request) else "", htmlpart), content_type = "text/html"
        )
    else:
        return HttpResponse("Empty")

def download(request, filename=None):
    try:
        password = request.GET['p']
    except:
        password = None
    # try:

    if FILEROOT is not None:
        files = list(os.walk(FILEROOT))[0][2]
        filesmd5 = name2md5(files)
        if filename not in filesmd5:
            return Http404()
        else: 
            filename = files[filesmd5.index(filename)]
            # print("!!!!\n", filename, "\n!!!!")
            if filename in passwords.keys():
                if password is None:
                    print(filename, type(filename))
                    return HttpResponse("""
                    <!DOCTYPE html>
                    <html>
                    <head>
                    <meta charset="utf-8" />
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <title>PolarisHub</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    </head>
                    <body>
                    <h1>{}</h1>
                    <h3>Password Required</h3>
                    <input id='pwd' onChange="changePassword()" />
                    <a href="" id='a'><button>Validate Password</button></a>
                    <script>
                        function changePassword(){{
                            var x = document.getElementById("pwd");
                            var y = document.getElementById('a');
                            console.log(x.value);
                            y.href = "?p=" + x.value;
                        }}
                    </script>
                    </body>
                    </html>
                    """.format(str(filename)), content_type="text/html")
                elif passwords[filename] != password:
                    return HttpResponse("Invalid Password")

            f = open(join(FILEROOT, filename), 'rb')
            response = FileResponse(f)
            response['Content-Type']='application/octet-stream'  
            response['Content-Disposition']='attachment;filename="{}"'.format(filename)
            return response
    return Http404()  
    # except:
    #     return HttpResponseServerError()

def hello(request):
    return HttpResponse('PolarisHub')

def changeAdminPassword(request):
    global settings
    if not checkIP(request):
        return HttpResponse("No Permission.")
    else:
        try:
            old_password = request.GET['oldp']
            new_password = request.GET['newp']
            if api.changeAdminPassword(old_password, new_password):
                settings = json.load(open(join(ROOT, 'settings.json'), 'r'))

                return HttpResponse("Change Password Success")
            else:
                return HttpResponse("Wrong Password")
        except:
            return HttpResponseServerError()

def changeSetting(request):
    global settings
    if not checkIP(request):
        return HttpResponse("No Permission.")
    else:
        try:
            key = request.GET["key"]
            key = key.replace(" ", "%20")
            value = request.GET['value']
            # password = request.GET['password']
            # print(key, value)
            if api.changeSettings(key, value, requirePassword=False):
                settings = json.load(open(join(ROOT, 'settings.json'), 'r'))

                return HttpResponse("Change Setting Success")
            else:
                return HttpResponse("Invalid admin password")
        except:
            return HttpResponseServerError()

def changePassword(request):
    global passwords
    if not checkIP(request):
        return HttpResponse("No Permission.")
    else:
        try:
            key = request.GET["key"]
            value = request.GET['value']
            # password = request.GET['password']
            # print(key, value)

            if api.changePasswords(key, value, requirePassword=False):
                passwords = json.load(open(join(ROOT, 'passwords.json'), 'r'))

                return HttpResponse("Change Passwords Success")
            else:
                return HttpResponse("Invalid admin password")
        except:
            return HttpResponseServerError()

def mySettings(request):
    
    if not checkIP(request):
        return HttpResponse("No Permission.")
    else:
        htmlpart = ''.join(["""<div style="display: flex; flex-direction: row;">
        <p id='p{0}' style="min-width:25rem"  >{1}</p>
        <input id='i{0}' style="margin: 0 2rem"   placeholder="{2}"></input>
        <button id='{0}' style="width: 10rem" onclick="changePassword({0})">Change Password</button>
        </div>""".format(i, item,  api.passwords[item] if item in api.passwords.keys() else "null" ) for (i, item) in enumerate(api.loadFileList())])
        settingspart = ''.join(["""<div style="display: flex; flex-direction: row;">
        <p id='p{0}' style="min-width:25rem"  >{1}</p>
        <input id='i{0}' style="margin: 0 2rem"   placeholder="{2}"></input>
        <button id='{0}' style="width: 10rem"  onclick="changesetting({0})">Change Setting</button>
        </div>""".format(i, item[0], item[1],) for (i, item) in enumerate(api.loadSettings().items())])
        return HttpResponse("""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <title>Settings</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                </head>
                <body>
                <style>
                    input, button { border-radius: .5rem; background: white; box-shadow: 2px 2px 1px rgba(0,0,0,0.3); height: 2rem; width: fit-content; }

                    input {width: 15rem; padding-left: 1rem}
                </style>
                    <a href="/">Back to homepage</a>
                    <h1>Settings</h1> 
                    <h3>Passwords</h3>
                    <p>null: no password</p>    
                    """+htmlpart+"""
                    <h3>Settings</h3>
                    """+settingspart+"""
                    <p>Hints:<br>
                            changeAdminPassword?oldp=___&newp=___<br>
                            changeSetting?key=___&value=___&password=___<br>
                            changePassword?key=___&value=___&password=___</p>
                    <script>
                        function changePassword(i){
                            var name = document.getElementById("p"+i).innerText;
                            var password = document.getElementById("i"+i).value;
                            console.log(name, password);
                            window.open("changePassword?key="+name+"&value="+password);
                        }
                        function changeSetting(i){
                            var name = document.getElementById("p"+i).innerText;
                            var value = document.getElementById("i"+i).value;
                            console.log(name, value);
                            window.open("changeSetting?key="+name+"&value="+value);
                        }
                    </script>
                </body>
                </html>""", content_type="text/html")

    # return HttpResponse("OK")

def checkIP(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META :
        ip =  request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']
    # print("IP: ", ip)
    return ip == "127.0.0.1"

def getQR(request):
    url = request.GET['url']
    filename = request.GET['filename']
    qr_name = generateCode(url, filename)
    return HttpResponse(open(qr_name, 'rb').read(), content_type="image/png")