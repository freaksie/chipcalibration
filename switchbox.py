import time
import urllib.request
from bs4 import BeautifulSoup
import json
response={
        'AC':'Connected ports: A-C, B-D',
        'BD':'Connected ports: A-C, B-D',
        'AB':'Connected ports: A-B, C-D',
        'CD':'Connected ports: A-B, C-D'
        }

def urlread(url):
    swread=urllib.request.urlopen(url).read()
    soup=BeautifulSoup(swread,'html.parser')
    connected_ports=soup.b.text.strip()
#    print(f'{connected_ports=}')
    return connected_ports
def urltoggle(url):
    connected_ports=urlread(url+"/?buttonToggle")
    return connected_ports
def connect(url,dest):
    connected_ports=urlread(url)
    while response[dest]!=connected_ports:
        urltoggle(url)
        time.sleep(1)
        connected_ports=urlread(url)
    return connected_ports

def rfswitch(board='huracan', chip='X6Y3'):
    with open('swcfg.json') as jfile:
        swcfg=json.load(jfile)
    for sw,dest in swcfg['boardchip'][board][chip].items():
        connect(url=swcfg['swurl'][sw],dest=dest)
    for sw in swcfg['swurl']:
        print(sw,urlread(swcfg['swurl'][sw]))

import argparse
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip','--ip',help='ip address for the switchbox',dest='ip',type=str,default="192.168.1.208")
    parser.add_argument('-t','--toggle',help='toggle current sw and read the final status',dest='toggle',default=False,action='store_true')
    parser.add_argument('-d','--dest',help='destinate switch status, AB,AC,BD,CD. ',dest='dest', choices=['AB','AC', 'BD','CD'],type=str,default=None)
    clargs=parser.parse_args()
    swurl='http://'+clargs.ip
    if clargs.toggle:
        urltoggle(swurl)
    if clargs.dest is not None:
        connect(url=swurl,dest=clargs.dest)
        #swread=(urlread(url=swurl))
        #while response[clargs.dest] not in swread:
        #    urltoggle(swurl)
        #    time.sleep(1)
        #    swread=str(urlread(url=swurl))
    print(f'{swurl}',urlread(url=swurl))
