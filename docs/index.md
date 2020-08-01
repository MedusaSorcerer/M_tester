
# M TEST
* service: `http://127.0.0.1:8080`
* version: `v0.0.0`
* result: [click](#result)


## <span id="login">Login</span>
* url: <code>http://127.0.0.1:8080/api/v0.0.0/login</code>
* method: <code>POST</code>
* status: <code id="server" style="">500</code>
* params: 
```text
{
    "password": "medusa",
    "username": "medusa"
}
```
* response:
```text
null
```
* error:
```text
Traceback (most recent call last):
  File "D:\Pythons\3.8.1\lib\site-packages\urllib3\connection.py", line 156, in _new_conn
    conn = connection.create_connection(
  File "D:\Pythons\3.8.1\lib\site-packages\urllib3\util\connection.py", line 84, in create_connection
    raise err
  File "D:\Pythons\3.8.1\lib\site-packages\urllib3\util\connection.py", line 74, in create_connection
    sock.connect(sa)
ConnectionRefusedError: [WinError 10061] 由于目标计算机积极拒绝，无法连接。
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "D:\Pythons\3.8.1\lib\site-packages\urllib3\connectionpool.py", line 665, in urlopen
    httplib_response = self._make_request(
  File "D:\Pythons\3.8.1\lib\site-packages\urllib3\connectionpool.py", line 387, in _make_request
    conn.request(method, url, **httplib_request_kw)
  File "D:\Pythons\3.8.1\lib\http\client.py", line 1230, in request
    self._send_request(method, url, body, headers, encode_chunked)
  File "D:\Pythons\3.8.1\lib\http\client.py", line 1276, in _send_request
    self.endheaders(body, encode_chunked=encode_chunked)
  File "D:\Pythons\3.8.1\lib\http\client.py", line 1225, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
  File "D:\Pythons\3.8.1\lib\http\client.py", line 1004, in _send_output
    self.send(msg)
  File "D:\Pythons\3.8.1\lib\http\client.py", line 944, in send
    self.connect()
  File "D:\Pythons\3.8.1\lib\site-packages\urllib3\connection.py", line 184, in connect
    conn = self._new_conn()
  File "D:\Pythons\3.8.1\lib\site-packages\urllib3\connection.py", line 168, in _new_conn
    raise NewConnectionError(
urllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPConnection object at 0x038E8778>: Failed to establish a new connection: [WinError 10061] 由于目标计算机积极拒绝，无法连接。
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "D:\Pythons\3.8.1\lib\site-packages\requests\adapters.py", line 439, in send
    resp = conn.urlopen(
  File "D:\Pythons\3.8.1\lib\site-packages\urllib3\connectionpool.py", line 719, in urlopen
    retries = retries.increment(
  File "D:\Pythons\3.8.1\lib\site-packages\urllib3\util\retry.py", line 436, in increment
    raise MaxRetryError(_pool, url, error or ResponseError(cause))
urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='127.0.0.1', port=8080): Max retries exceeded with url: /api/v0.0.0/login (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x038E8778>: Failed to establish a new connection: [WinError 10061] 由于目标计算机积极拒绝，无法连接。'))
During handling of the above exception, another exception occurred:
Traceback (most recent call last):
  File "D:/Django.py/tester/medusa.py", line 167, in main
    response = login(url, params)
  File "D:/Django.py/tester/medusa.py", line 88, in login
    return requests.post(url, data=params)
  File "D:\Pythons\3.8.1\lib\site-packages\requests\api.py", line 116, in post
    return request('post', url, data=data, json=json, **kwargs)
  File "D:\Pythons\3.8.1\lib\site-packages\requests\api.py", line 60, in request
    return session.request(method=method, url=url, **kwargs)
  File "D:\Pythons\3.8.1\lib\site-packages\requests\sessions.py", line 533, in request
    resp = self.send(prep, **send_kwargs)
  File "D:\Pythons\3.8.1\lib\site-packages\requests\sessions.py", line 646, in send
    r = adapter.send(request, **kwargs)
  File "D:\Pythons\3.8.1\lib\site-packages\requests\adapters.py", line 516, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPConnectionPool(host='127.0.0.1', port=8080): Max retries exceeded with url: /api/v0.0.0/login (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x038E8778>: Failed to establish a new connection: [WinError 10061] 由于目标计算机积极拒绝，无法连接。'))
```



<div id="dividing"></div>

## <span style="color: #107d00">Test Results</span>
| <font id="success">SUCCESS</font> | <font id="redirect">REDIRECT</font> | <font id="client">CLIENT ERROR</font> | <font id="server">SERVICE ERROR</font> |
| :---: | :---: | :---: | :---: |
|  |  |  | [Login](#login) |

<br>
<br>
<br>
<br>
<br>
