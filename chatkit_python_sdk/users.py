# coding=utf-8

import chatkit_python_sdk.base as base
import datetime

@base.response_extractor
def create_user(chatkit_access_data, user_id, name, avatar_url=None, custom_data=None):
    endpoint_parts = ["users"]

    user_data = {
        "id": user_id,
        "name": name
    }

    if(avatar_url is not None):
        user_data['avatar_url'] = avatar_url

    if(custom_data is not None):
        user_data['custom_data'] = custom_data

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="POST", json_parameters=user_data)

@base.response_extractor
def batch_create_users(chatkit_access_data, users):

    endpoint_parts = ["batch_users"]

    data = {"users": users}

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="POST", json_parameters=data)

@base.response_extractor
def get_user(chatkit_access_data, user_id):

    endpoint_parts = ["users", user_id]

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="GET")

@base.response_extractor
def get_users(chatkit_access_data, from_ts=None, limit=20):
    """
    from_ts: either a string in B8601DZw.d format or a UTC datetime object
    """

    endpoint_parts = ["users"]

    query_parameters = {
        "limit": limit
    }

    if(from_ts is not None):
        if(type(from_ts) == datetime.datetime):
            from_ts = from_ts.strftime("%Y-%m-%dT%H:%M:%S.Z")
        query_parameters['from_ts'] = from_ts

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="GET", query_parameters=query_parameters)

@base.response_extractor
def get_users_by_ids(chatkit_access_data, user_ids):
    endpoint_parts = ['users_by_ids']

    query_parameters = {
        'user_ids': ",".join(user_ids)
    }

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="GET", query_parameters=query_parameters)

@base.response_extractor
def update_user(chatkit_access_data, user_id, name=None, avatar_url=None, custom_data=None):

    endpoint_parts = ["users", user_id]

    parameters = {}

    if(name is not None):
        parameters['name'] = name

    if(avatar_url is not None):
        parameters['avatar_url'] = avatar_url

    if(custom_data is not None):
        parameters['custom_data'] = custom_data

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="PUT", json_parameters=parameters)

@base.response_extractor
def delete_user(chatkit_access_data, user_id):
    endpoint_parts = ["users", user_id]

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="DELETE")

@base.response_extractor
def get_user_rooms(chatkit_access_data, user_id, joinable=None):

    endpoint_parts = ["users", user_id, "rooms"]

    query_parameters = {}

    if(joinable is not None):
        query_parameters['joinable'] = bool(joinable)

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="GET", query_parameters=query_parameters)

@base.response_extractor
def join_room(chatkit_access_data, user_id, room_id):

    endpoint_parts = ["users", user_id, "rooms", room_id, "join"]

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="POST")

@base.response_extractor
def leave_room(chatkit_access_data, user_id, room_id):

    endpoint_parts = ["users", user_id, "rooms", room_id, "leave"]

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="POST")
