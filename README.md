# M Tester project

---

![](https://img.shields.io/badge/Python-3.8.1-red?&style=social)
![](https://img.shields.io/badge/mkdocs-1.1.2-red?&style=social)
![](https://img.shields.io/badge/Juejin.im-MedusaSorcerer-red?&style=social)

该项目主要是利用 Python 脚本实现 API 测试，并利用 mkdocs 服务器生成测试报告详情。

* 自动化测试 API 服务
* 生成测试数据报告
* 异常请求捕获
* 请求响应总览

### 项目逻辑
![](/docs/static/M-Tester-逻辑流程.png)

### medusa.py
这是项目的运行脚本文件，你只需要像其他 `.py` 文件一样运行即可：
```shell script
python3 medusa.py
```
其中有很多方法，当然你可能需要修改其中的逻辑问题：

| 函数名 | 说明 |
| :---: | --- |
| `get_url(url)` | 利用配置文件中的服务地址和指定前缀内容 + `url` 参数组合，返回完整的 API |
| `get_dict_key(data, keys)` | 该函数使用 `keys` 参数获取 `data` 的数据信息，如 `get_dict_key(data={"a": {"b": 1}}, keys="a.b")` 会返回 `1` |
| `get_result_dict(keys)` | 获取你的请求参数数据或者你的响应数据，需要使用制定格式 `[title].[METHOD].[request or response]`，如获取 Login 响应数据中的 `token` 字符：`Login.POST.response.token`，注意大小写 |
| `base_request(url, params, method)` | 根据 `url` 和 `params` 参数发送不同的 `method` 请求，并返回 response 对象 |
| `get_token(response)` | 接受一个 `response` 对象获取 `token` 字符串并添加前缀(JWT) |
| `login(url, params)` | 登陆的函数，注意你传递参数中，密码字段是否被加密 |
| `write_finish()` | 写入请求状态表格，对应界面中的 `Test Result` 菜单 |
| `json_text(js: [dict, str])` | 将传递的 `js` 对象进行格式化返回 |
| `write_result(url_title, url, method, params, status, response, error=None)` | 将每次请求的信息都写入到文件中<br>`url_title` 配置的 Title 字符串<br>`url` 请求的路径<br>`method` 请求方法<br>`params` 请求参数<br>`status` 响应状态<br>`response` 相应数据<br>`error=None` 错误信息 |
| `append_finish_list(status, title)` | 将指定的相应状态 `status` 的 `title` 添加到全局列表中 |
| `main()` | 入口函数 |

### MKDOCS 配置
项目目录文件 `mkdocs.yml` 是隶属于 mkdocs 服务的配置文件，如果你想自定义配置的各种属性，你可以[参考文档](https://markdown-docs-zh.readthedocs.io/zh_CN/latest/)并直接修改。

### PARAMS 配置
* `title` 项目最大路径的 title 字符串
* `version` 显示你的项目版本号，或用于 API 拼接
* `service` API访问服务地址：`127.0.0.1:8000`
* `login` 登陆的 URL 后缀地址
* `username` 登陆需要的用户名
* `password` 登陆需要的密码，若是需要加密，请指定加密后的字符
* `urls` 需要测试的 API 配置集合
    * `title` 请求的 Title 字符，如 `获取用户列表`、`Get Users List` 等
    * `url`: 请求的 URL 后缀字符串
    * `method` 请求方法，需要制定大写，并且支持 `GET`、`POST`、`DELETE`、`PUT`
    * `params` 需要传递的参数数据
    * `id` URL 参数的 id 说明对象

注意：
`params` 你可以使用 JSON 对象来说明你要传递的对象：
```yaml
params: {"key": "value"}
```
你也可以使用请求的 JSON 数据来指明你要传递的对象：
```yaml
# 传递已经请求的 title 为创建用户中的响应数据
params: '创建用户.POST.response'
```
你也可以使用请求的具体 JSON 对象中某个 KEY 下的数据：
```yaml
# 传递已经请求的 title 为创建用户的响应数据中的 username 字段
params: 
  username: '创建用户.POST.response.username'
```
# 你也可以组建自定义对象
```yaml
# 传递已经请求的 title 为创建用户的响应数据中的 username 字段 和 自定义 a 字段
params:
    username: '创建用户.POST.response.username'
    a: medusa
```

`id` 是一个映射了 URL 参数的对象，如：
```yaml
url: '/user/{user_id}'
```
我们预想的是请求 `/user/1` 这样的数据详情页，那你可以随意指明你的 id 表示字符，如上面的 `user_id`，你仅仅需要在 `id` 中对应的指明对象引用的数据即可：
```yaml
url: '/user/{user_id}'
id:
    user_id: 1
```
当然，上面的用法并没有什么意义，而我们使用的是这样的：
```yaml
title: 删除用户
url: '/user/{user_id}'
method: DELETE
id:
    user_id: '创建用户.POST.response.id'
```
使用创建用户的响应数据用的 id 字段的值来删除该用户，为测试数据不影响系统的数据内容。

> 如果请求的是个 `[]` 类型的数据，可能暂时无法获取其中的数据

### 样式配置
CSS 文件位于 `docs/static/medusa.css` 路径下，并且已经在 `mkdocs.yml` 文件中注册，你想自定样式的话，可以修改该文件。

### 其他
`lib` 文件夹下是用于写入 makedown 文件中的模板文件：
* `text_header.py` 写入头内容的模板
* `text_results.py` 写入每个请求的状态数据的模板
* `text_finish.py` 写入请求状态列表的模板
