# coding=utf-8

import chatkit_python_sdk.base as base

def set_cursor(chatkit_access_data, room_id, user_id, message_id):
    endpoint_parts = ['cursors', '0', 'rooms', room_id, 'users', user_id]

    parameters = {
        "position": message_id
    }

    return base.chatkit_cursor_request(chatkit_access_data, endpoint_parts, method="PUT", json_parameters=parameters)


def get_cursor(chatkit_access_data, room_id, user_id):

    endpoint_parts = ['cursors', '0', 'rooms', room_id, 'users', user_id]

    return base.chatkit_cursor_request(chatkit_access_data, endpoint_parts, method="GET")


def get_cursors_by_user(chatkit_access_data, user_id):
    endpoint_parts = ['cursors', '0', 'users', user_id]

    return base.chatkit_cursor_request(chatkit_access_data, endpoint_parts, method="GET")


def get_cursors_by_room(chatkit_access_data, room_id):

    endpoint_parts = ['cursors', '0', 'rooms', room_id]

    return base.chatkit_cursor_request(chatkit_access_data, endpoint_parts, method="GET")
