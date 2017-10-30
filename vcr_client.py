# -*- coding: utf-8 -*-
"""
vcr client
"""
import json
import logging
import requests
import bcesigner
import time


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


def media_speech(media_id):
    """
    :param media_id:
    :return:
    """
    request = get_request('GET', '/v1/media/{}'.format(media_id))
    request['params']['speech'] = ''
    request = generate_signature(request)
    return requests.get('{}{}?speech'.format(SERVER, request['uri']),
                        headers=request['headers'])


def media_character(media_id):
    """
    :param media_id:
    :return:
    """
    request = get_request('GET', '/v1/media/{}'.format(media_id))
    request['params']['character'] = ''
    request = generate_signature(request)
    return requests.get('{}{}?character'.format(SERVER, request['uri']),
                        headers=request['headers'])


def stream_post(stream_url, notification):
    """
    :param stream_url: stream url
    :param notification: notification
    :return:
    """
    request = get_request('POST', '/v1/stream')
    request = generate_signature(request)
    payload = {
        'source': stream_url,
        'notification': notification
    }
    return requests.post('{}{}'.format(SERVER, request['uri']), 
                        data=json.dumps(payload),
                        headers=request['headers'])


def stream_get(stream_url, start_time, end_time):
    """
    :param stream_url: stream url
    :param start_time: utc time, e.g. 2017-07-24T13:37:10Z
    :param end_time: utc time
    :return: stream check result
    """
    request = get_request('GET', '/v1/stream')
    request['params']['source'] = stream_url
    request['params']['startTime'] = start_time
    request['params']['endTime'] = end_time
    request = generate_signature(request)
    return requests.get('{}{}?source={}&startTime={}&endTime={}'.format(SERVER, 
        request['uri'], stream_url, start_time, end_time), headers=request['headers'])


def image_put(source):
    """
    :param source:
    :return:
    """
    request = get_request('PUT', '/v1/image')
    request = generate_signature(request)
    payload = {
        'source': source
    }
    return requests.put('{}{}'.format(SERVER, request['uri']),
                        data=json.dumps(payload),
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
    # ---- check media ----
    response = media_put("YourMediaId")
    if response.status_code == 200:
        print "congratulations!"
    else:
        print "put media error:", response.json()

    # wait for media check response notification or
    # use media_get to query vcr check result.
    # response = media_get("YourMediaId")
    # print response.json()

    # ---- check stream ----
    # stream_url = "YourStreamUrl"
    # response = stream_post(stream_url, "YourNotificationName")
    # if response.status_code == 200:
    #     print "congratulations!"
    # else:
    #     print "put stream error:", response.json()
    
    # wait for stream check notification or
    # use stream_get to query stream check result
    # while True:
    #     response = stream_get(stream_url, '2017-10-23T00:00:00Z', '2017-10-23T16:00:00Z')
    #     if response.status_code == 200:
    #         print "stream check result:", response.json()
    #     else:
    #         print "get stream check result error:", response.json()
    #     time.sleep(5)

    # ---- check image ----
    # source format: bos://{bucket}/{object} or url
    # image_source = "YourImageSource" 
    # response = image_put(image_source)
    # print response.json()

    # ---- check text ----
    # text = "YourText"
    # response = text_put(image_source)
    # print response.json()