# coding=utf-8

import requests
import time
import jwt
import urllib
import copy

import sys

"""
a decorator to extract the result (json/text) of a request
"""
def response_extractor(request_function):
    def wrapper(*args, **kwargs):
        result = None

        res = request_function(*args, **kwargs)

        res.raise_for_status()

        try:
            result = res.json()
        except Exception:
            result = res.text
        
        return result
    
    return wrapper


def build_specific_endpoint(parts):
    str_parts = list(map(lambda x : urllib.quote_plus(str(x)), parts))
    return "/".join(str_parts)


def _chatkit_request(chatkit_access_data, base_endpoint, endpoint_parts, query_parameters={}, json_parameters={}, headers={}, method="GET", files=None):
    endpoint = build_specific_endpoint(endpoint_parts)

    hdrs = copy.deepcopy(chatkit_access_data.base_headers)

    if(
        method in ["POST", "PUT"]
        and json_parameters not in [[], {}, None]
        and 'Content-Type' not in map(lambda x: x.title(), headers.keys())
    ):
        hdrs.update({"Content-Type": "application/json"})

    hdrs.update(headers)

    full_endpoint = base_endpoint + "/" + endpoint

    if(method == "POST" and files is None):
        return requests.post(full_endpoint, headers=hdrs, json=json_parameters)
    elif(method == "POST" and files is not None):
        return requests.post(full_endpoint, files=files)
    elif(method == "GET"):
        return requests.get(full_endpoint, headers=hdrs, params=query_parameters)
    elif(method == "PUT"):
        return requests.put(full_endpoint, headers=hdrs, json=json_parameters)
    elif(method == "DELETE"):
        return requests.delete(full_endpoint, headers=hdrs, params=query_parameters)


def chatkit_request(chatkit_access_data, endpoint_parts, query_parameters={}, json_parameters={}, headers={}, method="GET"):
    base_chat_endpoint = chatkit_access_data.base_endpoint + "/chatkit/v1/" + chatkit_access_data.instance_id
    return _chatkit_request(
        chatkit_access_data=chatkit_access_data,
        base_endpoint=base_chat_endpoint,
        endpoint_parts=endpoint_parts,
        query_parameters=query_parameters,
        json_parameters=json_parameters,
        headers=headers,
        method=method
    )


def chatkit_auth_request(chatkit_access_data, endpoint_parts, query_parameters={}, json_parameters={}, headers={}, method="GET"):
    base_auth_endpoint = chatkit_access_data.base_endpoint + "/chatkit_authorizer/v1/" + chatkit_access_data.instance_id
    return _chatkit_request(
        chatkit_access_data=chatkit_access_data,
        base_endpoint=base_auth_endpoint,
        endpoint_parts=endpoint_parts,
        query_parameters=query_parameters,
        json_parameters=json_parameters,
        headers=headers,
        method=method
    )


def chatkit_file_request(chatkit_access_data, endpoint_parts, query_parameters={}, json_parameters={}, headers={}, method="GET", files=None):
    base_files_endpoint = chatkit_access_data.base_endpoint + "/chatkit_files/v1/" + chatkit_access_data.instance_id
    return _chatkit_request(
        chatkit_access_data=chatkit_access_data,
        base_endpoint=base_files_endpoint,
        endpoint_parts=endpoint_parts,
        query_parameters=query_parameters,
        json_parameters=json_parameters,
        headers=headers,
        method=method,
        files=None
    )

def chatkit_cursor_request(chatkit_access_data, endpoint_parts, query_parameters={}, json_parameters={}, headers={}, method="GET", files=None):
    base_files_endpoint = chatkit_access_data.base_endpoint + "/chatkit_cursors/v1/" + chatkit_access_data.instance_id
    return _chatkit_request(
        chatkit_access_data=chatkit_access_data,
        base_endpoint=base_files_endpoint,
        endpoint_parts=endpoint_parts,
        query_parameters=query_parameters,
        json_parameters=json_parameters,
        headers=headers,
        method=method,
        files=None
    )


def build_token(instance_id, key_id, key_secret, user_id=None, su=False, token_ttl=None, expire_timestamp=None, issue_timestamp=None):
    su = bool(su)

    if(token_ttl is None or int(token_ttl) <= 0):
        token_ttl = 86400

    token_ttl = int(token_ttl)
    
    if(issue_timestamp is None):
        issue_timestamp = int(time.time())

    expire_timestamp = issue_timestamp + token_ttl

    payload = {
        'exp': expire_timestamp,
        'iat': issue_timestamp,
        'instance': instance_id,
        'iss': 'api_keys/' + key_id,
        'su': su
    }

    if(user_id is not None):
        payload['sub'] = user_id

    encoded = jwt.encode(payload, key_secret, algorithm='HS256')

    return encoded, su, issue_timestamp, token_ttl, expire_timestamp


def decode_token(passed_token, key_secret):
    try:
        return jwt.decode(passed_token, key_secret, algorithms=['HS256'])
    except Exception:
        return None


def init_headers(instance_id, key_id, key_secret, user_id=None, superuser=False):
    access_token, _, _, _, _= build_token(instance_id, key_id, key_secret, user_id=user_id, su=bool(superuser))
    return {'Authorization': 'Bearer ' + access_token}


def split_instance(instance):
    result = instance.split(":")

    version = result[0]
    region = result[1]
    instance_id = result[2]

    return version, region, instance_id


def split_secret(secret):

    result = secret.split(":")

    key_id = result[0]
    key_secret = result[1]

    return key_id, key_secret

class ChatkitAccessData(object):
    base_endpoint = "https://us1.pusherplatform.io/services"

    def __init__(self, secret, instance, user_id=None, expire_timestamp=None, issue_timestamp=None, superuser=False):
        self.key_id, self.key_secret = split_secret(secret)

        self.version, self.region, self.instance_id = split_instance(instance)

        self.user_id = user_id

        self.access_token, self.su_access_token, self.issue_timestamp, self.token_expires_in, self.expire_timestamp = build_token(
            instance_id=self.instance_id,
            key_id=self.key_id,
            key_secret=self.key_secret,
            user_id=user_id,
            expire_timestamp=expire_timestamp,
            issue_timestamp=issue_timestamp,
            su=bool(superuser)
        )

        self.base_headers = init_headers(self.instance_id, self.key_id, self.key_secret, user_id=user_id, superuser=superuser)

    def verify_token(self, passed_token, chatkit_user_id):
        time_now = time.time()

        return (
            self.access_token == passed_token
            and self.user_id == chatkit_user_id
            and self.expire_timestamp >= time.time()
        )
