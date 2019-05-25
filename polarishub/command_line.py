from polarishub import setup
from polarishub import manage
import sys, os
def operation():
    setup.initialization()

from polarishub import manage
def runHub():
    #print(sys.argv)
    s = "from polarishub import manage\nmanage.runserver()"
    file = open("testHub.py", "w")
    file.write(s)
    file.close()
    r = os.popen("python -V")
    text = r.read()
    r.close()
    if text:
        if text.startswith("Python 3"):
            os.system("python testHub.py")
    else:
        r = os.popen("python3 -V")
        text2 = r.read()
        r.close()
        if text2:
            os.system("python3 testHub.py")
        else:
            print("Polarishub don't support python2. Sorry.")

def main():
    commandArgv = sys.argv
    if len(commandArgv) == 1:
        print("Wrong command! Please use -h for help.")
        return
    if commandArgv[1] == "-h":
        print("Commands:")
        print("  setup:\tSetup the environment for polarishub.")
        print("  run:\trun the polarishub on your computer.")
    if commandArgv[1] == "setup":
        operation()
    if commandArgv[1] == "run":
        runHub()