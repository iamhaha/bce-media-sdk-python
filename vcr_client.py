# -*- coding: utf-8 -*-
"""
vcr client
"""
import json
import logging
import requests
import bcesigner


SERVER = 'http://vcr.bj.baidubce.com'
HOST = 'vcr.bj.baidubce.com'
ACCESS_KEY = 'YourAK'
SECRET_KEY = 'YourSK'


def generate_signature(request):
    """
    :param request:
    :return:
    """
    signer = bcesigner.BceSigner(ACCESS_KEY, SECRET_KEY)
    signer.logger.setLevel(logging.WARNING)
    auth = signer.gen_authorization(request, timestamp=None, expire_period=3600)

    request['headers']['authorization'] = auth
    request['headers']['content-type'] = 'application/json'

    return request


def get_request(method='', uri=''):
    """
    :param method:
    :param uri:
    :return:
    """
    return {
        'method': method,
        'uri': uri,
        'params': {
        },
        'headers': {
            'host': HOST,
            'content-type': 'application/json'
        }
    }


def text_put(text):
    """
    :param text:
    :return:
    """
    request = get_request('PUT', '/v1/text')
    request = generate_signature(request)
    payload = {
        'text': text
    }
    return requests.put('{}{}'.format(SERVER, request['uri']),
                        data=json.dumps(payload),
                        headers=request['headers'])


if __name__ == "__main__":
    response = text_put("这是一段待审核文本")
    print response.json()