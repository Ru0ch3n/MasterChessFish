from selenium import webdriver
import subprocess
from time import sleep
import os
from pystockfish import *

deep = Engine(depth=14)
path = os.path.split(os.path.realpath(__file__))[0]
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["enable-logging"])
browser = webdriver.Chrome(executable_path ="F:\\chromedriver_win32\\chromedriver.exe", chrome_options=options)
filename = 'capture.png'
#browser.get("https://www.chess.com/")
browser.set_window_size(1000,800)
browser.set_window_position(0,0)
puzzle = 'y'
FEN = ''
color = 'w'
def __external_cmd(cmd, code="utf8"):
    global FEN
    print(cmd)
    process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    flag = False
    while process.poll() is None:
        line = process.stdout.readline()
        line = line.strip()
        if line:
            line = line.decode(code, 'ignore')
            if flag:
                FEN = line
                if color == 'b':
                    print('before replace:')
                    print(FEN)
                    print('replace:')
                    FEN = FEN.replace('0 1 ','1 0')
                    FEN = FEN.replace(' w ',' b')
                flag = False
            if "Predicted" in line:
                flag = True

color = input('White or Black?(w/b)')
while(True):
    if puzzle == 'y':
        color = input('White or Black?(w/b)')
    else:
        sleep(1)
    browser.save_screenshot(filename)
    __external_cmd(('python ' + path +'\\tensorflow_chessbot.py --filepath ' + path + '\\capture.png').replace('\\\\','\\'))
    deep.setfenposition(FEN)
    print(FEN)
    best = deep.bestmove()['move']
    print(best)