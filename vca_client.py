# -*- coding: utf-8 -*-
"""
vca client
"""

import requests
import json
import logging
import bcesigner


SERVER = 'http://vca.bj.baidubce.com'
HOST = 'vca.bj.baidubce.com'
ACCESS_KEY = 'YourAk'
SECRET_KEY = 'YourSk'


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


def filter_none_value_for_dict(my_dict):
    """ filter none value """
    return dict((key, value) for key, value in my_dict.items() if value is not None and len(value))


def get_pretty_print(json_object):
    """ print json """
    return json.dumps(json_object, sort_keys=True, indent=4,
                      separators=(',', ': '), ensure_ascii=False)


def media_get(media_id):
    """
    :params: media_id
    :return: media analysis result
    """

    request = get_request('GET', '/v1/media/{}'.format(media_id))
    request = generate_signature(request)
    return requests.get('{}{}'.format(SERVER, request['uri']), headers=request['headers'])


def media_put(media_id, preset=None, notification=None):
    """
    :params: media_id
    :params: preset
    :params: notification
    :return: success
    """

    request = get_request('PUT', '/v1/media/{}'.format(media_id))
    request = generate_signature(request)
    payload = {
        'mediaId': media_id,
        'preset': preset,
        'notification': notification
    }
    payload = filter_none_value_for_dict(payload)
    return requests.put('{}{}'.format(SERVER, request['uri']),
                        data=json.dumps(payload), headers=request['headers'])


def media_put_v2(source, preset=None, notification=None):
    """
    :params: source
    :params: preset
    :params: notification
    :return: success
    """

    request = get_request('PUT', '/v2/media')
    payload = {
        "source": source,
        "preset": preset,
        "notification": notification
    }
    payload = filter_none_value_for_dict(payload)
    request = generate_signature(request)
    return requests.put('{}{}'.format(SERVER, request['uri']),
                        data=json.dumps(payload), headers=request['headers'])


def media_get_v2(source):
    """
    :params: source
    :return: media analysis result
    """

    request = get_request('GET', '/v2/media')
    request['params']['source'] = source
    request = generate_signature(request)
    return requests.get('{}{}?source={}'.format(SERVER, request['uri'], source),
                        headers=request['headers'])


if __name__ == "__main__":
    # ---- analyze media v1 ----
    response = media_put("YourMediaId")
    # response = media_put("YourMediaId", "YourPreset")
    # response = media_put("YourMediaId", "YourPreset", "YourNotification")
    if response.status_code == 200:
        print "congratulations!"
    else:
        print "put media error:", response.json()

    # pass

    # wait for media check response notification or
    # use media_get to query vca analysis result.
    # response = media_get("YourMediaId")
    # print get_pretty_print(response.json())

    # ---- analyze media v2 ----
    # response = media_put_v2("YourMediaSource")
    # response = media_put("YourMediaSource", "YourPreset")
    # response = media_put("YourMediaSource", "YourPreset", "YourNotification")
    # if response.status_code == 200:
    #     print "congratulations!"
    # else:
    #     print "put media error:", response.json()

    # pass

    # wait for media check response notification or
    # use media_get to query vca analysis result.
    # response = media_get_v2("YourMediaSource")
    # print get_pretty_print(response.json())
