#关闭证书验证，但这是不合适的，我之后会在Agent上加证书:(
import twisted.internet._sslverify as v

v.platformTrust = lambda: None