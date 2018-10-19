# coding=utf-8

import chatkit_python_sdk.base as base

@base.response_extractor
def create_room(chatkit_access_data, name, private=True, user_ids=[]):

    endpoint_parts = ["rooms"]

    parameters = {
        "private": bool(private)
    }

    parameters['name'] = name

    if(user_ids not in [None, []]):
        parameters['user_ids'] = user_ids

    return base.chatkit_request(chatkit_access_data, endpoint_parts, json_parameters=parameters, method="POST")

@base.response_extractor
def fetch_room(chatkit_access_data, room_id):
    endpoint_parts = ['rooms', room_id]

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="GET")

@base.response_extractor
def fetch_rooms(chatkit_access_data, from_id=None, include_private=False):

    endpoint_parts=['rooms']

    query_parameters = {}

    if(from_id is not None):
        query_parameters['from_id'] = from_id

    if(include_private is not None):
        query_parameters['include_private'] = 'true' if bool(include_private) else 'false'

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method='GET', query_parameters=query_parameters)

@base.response_extractor
def delete_room(chatkit_access_data, room_id):
    endpoint_parts = ["rooms", room_id]

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="DELETE")

@base.response_extractor
def update_room(chatkit_access_data, room_id, name=None, private=None):
    parameters = {}

    endpoint_parts = ['rooms', room_id]

    if(name is not None):
        parameters['name'] = name

    if(private is not None):
        parameters['private'] = bool(private)

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="PUT", json_parameters=parameters)

@base.response_extractor
def add_users(chatkit_access_data, room_id, user_ids=[]):
    endpoint_parts = ['rooms', room_id, 'users', 'add']

    parameters = {
        "user_ids": user_ids
    }

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="PUT", json_parameters=parameters)

@base.response_extractor
def remove_users(chatkit_access_data, room_id, user_ids=[]):
    endpoint_parts = ['rooms', room_id, 'users', 'remove']

    parameters = {
        "user_ids": user_ids
    }

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="PUT", json_parameters=parameters)


@base.response_extractor
def leave_room(chatkit_access_data, room_id, user_id):
    endpoint_parts = ['users', user_id, 'rooms', room_id, 'leave']

    parameters = {
    }

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="POST", json_parameters=parameters)

