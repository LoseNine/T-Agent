# Tagent
Using the Twisted Web Client

Tagent 是一个对于Twisted Web Client的整合

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

* <small>proxyRequest<small>

### 使用说明

### Theaders

> 用于格式化headers，以及添加自定义的headers头部

### App get
```python
def main(reactor, *args):
    t=Tclient(method='GET',url='http://baidu.com')
    d=t.get()
    d.addCallback(print_result)
    return d
```

### App post
```python
def main(reactor, *args):
    t=Tclient(method='POST',url='http://httpbin.org/post',data=json.dumps({"msg": "Twisted"}).encode('ascii'))
    d=t.post()
    d.addCallback(print_result)
    return d
```

### App proxy
```python
def main(reactor, *args):
    t=Tclient(method='GET',url='http://baidu.com',proxy={'http://111.79.198.127':'9999'})
    d=t.get()
    d.addCallback(print_result)
    return d
```

### App verify
```python
def main(reactor, *args):
    t=Tclient(method='GET',url='https://github.com',verify=False)
    d=t.get()
    d.addCallback(print_result)
    return d
```


