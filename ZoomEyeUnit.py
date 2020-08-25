#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Author spkiddai
"""

import json
import requests
import configparser

class ZoomEyeUnit():

    def __init__(self):
        self.config = self.read_config()#读取配置文件配置
        self.headers = self.create_token() #生成Access_TOKEN的header

#配置文件内容 用户、密码、API接口地址
    def read_config(self):
        result = {}
        config = configparser.ConfigParser()
        config.read("Config.ini")
        result['user'] = config['ZoomEye Login']['USER']
        result['pass'] = config['ZoomEye Login']['PASS']
        result['login'] = config['ZoomEye API']['Login']
        result['info'] = config['ZoomEye API']['Info']
        result['host'] = config['ZoomEye API']['Host']
        result['web'] = config['ZoomEye API']['Web']
        return result

#生成Token，用户名密码登录login接口
    def create_token(self):
        data = json.dumps({"username":self.config['user'],"password":self.config['pass']})
        response = self.req_post(self.config['login'],data=data)
        header = {"Authorization": "JWT %s" % (response["access_token"])}
        return header

#用户信息接口：无需参数传入
    def info(self):
        response = ZoomEyeUnit.req_get(self.config['info'],header=self.headers)
        return response

#主机搜索接口：需传入参数 query查询表达式 示例：prrt:8080   page页码 示例：1  facets排序 示例：app,os
    def Host_search(self,query,page=None,facets=None):
        params = {"query" : query }
        if page:
            params.update({"page" : str(page)})
        if facets:
            params.update({"facets" : facets})
        response = self.req_get(self.config['host'],params,self.headers)
        return response

#Web搜索接口：需传入参数 query查询表达式 示例：prrt:8080   page页码 示例：1  facets排序 示例：app,os
    def Web_search(self,query,page=None,facets=None):
        params = { "query" : query }
        if page:
            params.update({"page" : str(page)})
        if facets:
            params.update({"facets" : facets})
        response = self.req_get(self.config['web'],params,self.headers)
        return response

    @staticmethod
    def req_get(url, params=None, header=None):
        try:
            response = requests.get(url=url, params=params, headers=header)
            if response.status_code == 200:
                return response.json()
            else:
                print('[-ERROR]:' + str(response.status_code) + response.text)
                exit(0)
        except Exception as e:
            raise ('[-ERROR]:' + e)

    @staticmethod
    def req_post(url, data, header=None):
        try:
            response = requests.post(url=url, data=data, headers=header)
            if response.status_code == 200:
                return response.json()
            else:
                print('[-ERROR]:' + str(response.status_code) + response.text)
                exit(0)
        except Exception as e:
            raise ('[-ERROR]:' + e)
