# T-Agent
Using the Twisted Web Client

T-Agent 是一个对于Twisted Web Client的整合

### 功能介绍

目前实现

* get
* post
* downpage
* contentDecodeRequest：

        Adds support for sending Accept-Encoding request headers and interpreting Content-Encoding response headers.
        
* cookieRequest：

        Be used to store the cookie information.
        
* redirectRequest ：

        Following redirects，it implements a rather strict behavior of the RFC.
        
* proxyRequest ：

        Using a HTTP proxy.
        
        
* startlog :

        Start log.
        
* randomHeader : 

        Random choice a User-Agent

目前T-Agent里也只有三个小模块：

* app
* Tagent
* Theaders

### 使用说明

### Theaders

> 用于格式化headers

# 注意！要包裹在 [] 而且是 byte
```python
class TgerHeaders:
    def __init__(self):
        self.headPool=[{b'User-Agent':[b'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML,likeGecko)Chrome/63.0.3239.26Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400']},
                       {b'User-Agent': [b'Twisted WebBot'],}]
```

