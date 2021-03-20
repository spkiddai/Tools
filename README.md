# ZoomEyeUnit

## 配置文件：
[ZoomEye Login]
USER = test
PASS = test
 
[ZoomEye API]
Login = https://api.zoomeye.org/user/login
Info = https://api.zoomeye.org/resources-info
Host = https://api.zoomeye.org/host/search
Web = https://api.zoomeye.org/web/search


## 调用方法：

z = ZoomEyeUnit()
result = z.Host_search("port:8080"",page=1)
print(result)
