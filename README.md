# T-Agent
Using the Twisted Web Client

T-Agent 是一个对于Twisted Web Client的整合

实现类似requests的东西

### 功能介绍

目前实现

* get
* post
* downpage
* contentDecodeRequest
* cookieRequest    
* redirectRequest 
* startlog
* randomHeader
* verify

* proxyRequest

### 使用说明

### Theaders

> 用于格式化headers，以及添加自定义的headers头部

### App get
```python
def main(reactor, *args):
    t=Tclient(method='GET',url='http://baidu.com',timeout=3,verify=False)
    d=t.get()
    d=t.execute(d)
    d.addCallback(print_result)
    return d
```

### App post
```python
def main(reactor, *args):
    t=Tclient(method='POST',url='http://httpbin.org/post',data=json.dumps({"msg": "Twisted"}).encode('ascii'))
    d=t.post()
    d=t.execute(d)
    d.addCallback(print_result)
    return d
```


