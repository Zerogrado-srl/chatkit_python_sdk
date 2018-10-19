# coding=utf-8

import chatkit_python_sdk.base as base


def send_message(chatkit_access_data, room_id, text, attachment_resource_link=None, attachment_type=None):
    """
    attachment_resource_link:a valid url
    attachment_type: one of ['image', 'video', 'audio', 'file']
    """

    endpoint_parts = ["rooms", room_id, "messages"]

    parameters = {
        "text": text
    }

    if(attachment_type is not None and attachment_resource_link is not None):
        parameters['attachment'] = {
            'resource_link': attachment_resource_link,
            'type': attachment_type
        }

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="POST", json_parameters=parameters)


def fetch_messages(chatkit_access_data, room_id, initial_id=None, limit=20, direction="newer"):
    """
    direction in ['newer', 'older']
    """
    endpoint_parts = ["rooms", room_id, "messages"]

    query_parameters = {}

    if(initial_id is not None):
        query_parameters['initial_id'] = initial_id

    if(limit is not None):
        query_parameters['limit'] = limit

    if(direction is not None):
        query_parameters['direction'] = direction

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="GET", query_parameters=query_parameters)


def typing_indicators(chatkit_access_data, room_id, start=True, data={}):
    endpoint_parts = ["rooms", room_id, "events"]

    parameters = {
        "name": "typing_start" if(bool(start) is True) else "typing_stop"
    }

    if(data not in [[], {}]):
        parameters['data'] = data

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="POST", json_parameters=parameters)


def delete_message(chatkit_access_data, message_id):
    endpoint_parts = ["messages", message_id]

    return base.chatkit_request(chatkit_access_data, endpoint_parts, method="DELETE")
