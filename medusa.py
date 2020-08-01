#!/usr/bin/env python
# _*_ Coding: UTF-8 _*_
import json
import re
import time
from json.decoder import JSONDecodeError
from traceback import format_exc

import requests
import yaml

try:
    from lib.text_header import text as header
    from lib.text_results import text as results
    from lib.text_finish import text as finish
except ImportError:
    print('import error')
    header, results, finish = '', '', ''


def get_url(url):
    return service + '/api/' + version + url


def get_dict_key(data, keys):
    if not keys: return data
    d = keys.split('.')
    if d[1:]:
        return get_dict_key(data[d[0]], '.'.join(d[1:]))
    return data[d[0]]


def get_result_dict(keys):
    """ [title].[method].[request|response] """

    def _list_handler(_v):
        _value = list()
        for _i in _v:
            if isinstance(_i, list):
                _value.append(_list_handler(_i))
            elif isinstance(_i, dict):
                _value.append(_dict_handler(_i))
            elif isinstance(_i, str):
                _value.append(_str_handler(_i))
            else:
                _value.append(_i)
        return _value

    def _str_handler(_v):
        _regex = re.match(r'^(.*)\.(GET|POST|PUT|DELETE)\.(request|response)(\.(.*))?', _v)
        if _regex:
            return get_dict_key(results_dict[_regex.group(1)][_regex.group(2)][_regex.group(3)], _regex.group(5))
        return _v

    def _dict_handler(_v):
        _value = dict()
        for _k, _ in _v.items():
            if isinstance(_, str):
                _ = _str_handler(_)
            elif isinstance(_, list):
                _ = _list_handler(_)
            elif isinstance(_, dict):
                _ = _dict_handler(_)
            _value[_k] = _
        return _value

    if isinstance(keys, dict):
        return _dict_handler(keys)
    if isinstance(keys, list):
        return _list_handler(keys)
    if isinstance(keys, str):
        return _str_handler(keys)
    return keys


def base_request(url, params, method):
    if method.upper() == 'GET':
        return requests.get(url, params=params, headers={'Authorization': token})
    if method.upper() in ('POST', 'PUT', 'DELETE'):
        return getattr(requests, method.lower())(url, json=params, headers={'Authorization': token})


def get_token(response):
    return 'jwt ' + response.json()['detail']['jdooootoken']


def login(url, params):
    return requests.post(url, data=params)


def write_finish():
    mdf.write(finish.format(
        '<br>'.join(success),
        '<br>'.join(redirect),
        '<br>'.join(clienterr),
        '<br>'.join(serviceerr),
    ))


def json_text(js: [dict, str]):
    if not js:
        return "null"
    try:
        if isinstance(js, dict):
            return json.dumps(js, sort_keys=True, indent=4, ensure_ascii=False)
        return json.dumps(json.loads(js), sort_keys=True, indent=4, ensure_ascii=False)
    except (json.decoder.JSONDecodeError, TypeError):
        return re.sub('(\n|\r\n)+', '\n', str(js)).strip('\n')


def write_result(url_title, url, method, params, status, response, error=None):
    if status >= 500:
        code_id = 'server'
    elif status >= 400:
        code_id = 'client'
    elif status >= 300:
        code_id = 'redirect'
    else:
        code_id = 'success'
    msg = json_text(f"""* error:\n```text\n{error}\n```\n""") if error else ''
    mdf.write(results.format(
        str(url_title).lower().replace(' ', '-'),
        url_title,
        url,
        method,
        code_id,
        status,
        json_text(params),
        json_text(response),
        msg,
    ))


def append_finish_list(status, title):
    info = f'[{title}](#{title.lower().replace(" ", "-")})'
    if status >= 500:
        serviceerr.append(info)
    elif status >= 400:
        clienterr.append(info)
    elif status >= 300:
        redirect.append(info)
    elif status >= 200:
        success.append(info)


def main():
    # configure file
    yf = open('docs/params.yaml', 'r', encoding='UTF-8')
    config = yaml.safe_load(yf.read())
    yf.close()

    # global variable
    global service, token, mdf, results_dict, version, success, redirect, clienterr, serviceerr
    success, redirect, clienterr, serviceerr = [], [], [], []
    results_dict = dict()
    version = config['version']
    service = f'http://' + config['service']
    mdf = open('docs/index.md', 'w', encoding='UTF-8')

    # write header text
    mdf.write(header.format(config['title'], service, version))

    # login request
    url = get_url(config["login"])
    params = {'username': config['username'], 'password': config['password']}
    try:
        response = login(url, params)
    except (Exception,):
        write_result(
            url_title='Login',
            url=url,
            method='POST',
            params=params,
            status=500,
            response=None,
            error=str(format_exc()),
        )
        append_finish_list(500, 'Login')
        write_finish()
        mdf.close()
        return
    write_result(
        url_title='Login',
        url=url,
        method='POST',
        params=params,
        status=response.status_code,
        response=response.text
    )
    append_finish_list(response.status_code, 'Login')
    if response.status_code != 200:
        write_finish()
        mdf.close()
        return

    # get token string
    token = get_token(response)

    # other configure request
    for i in config['urls']:
        time.sleep(.5)
        url, params = get_url(i['url']), i.get('params')
        if re.search(r'{.*}', url):
            try:
                url = url.format(**get_result_dict(i['id']))
            except Exception as e:
                print(f'analyze URL error({i["title"]}): {e}')
                write_result(
                    url_title=i['title'],
                    url=url,
                    method=i['method'],
                    params='未解析',
                    status=500,
                    response=None,
                    error=str(format_exc()),
                )
                continue
        try:
            if params: params = get_result_dict(params)
            if i['title'] not in list(results_dict.keys()):
                results_dict[i['title']] = dict()
            if i['method'] not in list(results_dict[i['title']].keys()):
                results_dict[i['title']][i['method']] = dict()
            results_dict[i['title']][i['method']]['request'] = params
        except Exception as e:
            print(f'save request error({i["title"]}): {e}')
        try:
            response = base_request(url=url, method=i['method'], params=params)
        except (Exception,):
            write_result(
                url_title=i['title'],
                url=url,
                method=i['method'],
                params=params,
                status=500,
                response=None,
                error=str(format_exc()),
            )
            append_finish_list(500, i['title'])
        else:
            if response is not None:
                write_result(
                    url_title=i['title'],
                    url=url,
                    method=i['method'],
                    params=params,
                    status=response.status_code,
                    response=response.text
                )
                if 200 <= response.status_code < 300:
                    try:
                        if i['title'] not in list(results_dict.keys()):
                            results_dict[i['title']] = dict()
                        if i['method'] not in list(results_dict[i['title']].keys()):
                            results_dict[i['title']][i['method']] = dict()
                        results_dict[i['title']][i['method']]['response'] = response.json()
                    except JSONDecodeError:
                        pass
                    except Exception as e:
                        print(f'save response error({i["title"]}): {e}')
                append_finish_list(response.status_code, i['title'])
            else:
                append_finish_list(500, i['title'])
                write_result(
                    url_title=i['title'],
                    url=url,
                    method=i['method'],
                    params=params,
                    status=500,
                    response=f'请求方法不支持：{i["method"]}'
                )
    write_finish()
    mdf.close()


if __name__ == '__main__':
    main()
