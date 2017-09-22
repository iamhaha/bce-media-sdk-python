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


def media_put(media_id, notification=None):
    """
    :param media_id: vod media id
    :param notification: callback notification
    :return:
    """
    request = get_request('PUT', '/v1/media/{}'.format(media_id))
    if notification is None:
        notification = ''
    request['params']['notification'] = notification
    request = generate_signature(request)
    return requests.put('{}{}?notification={}'.format(SERVER, request['uri'], notification),
                        headers=request['headers'])


def media_get(media_id):
    """
    :param media_id: vod media id
    :return:
    """
    request = get_request('GET', '/v1/media/{}'.format(media_id))
    request = generate_signature(request)
    return requests.get('{}{}'.format(SERVER, request['uri']),
                        headers=request['headers'])


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
    response = media_put("YourMediaId")
    if response.status_code == 200:
        print "congratulations!"
    else:
        print "put media error:", response.json()
    # wait for media check response notification or
    # use media_get to query vcr check result.
    # response = media_get("YourMediaId")
    # print response.json()