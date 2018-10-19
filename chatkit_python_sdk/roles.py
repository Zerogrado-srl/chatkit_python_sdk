# coding=utf-8

import chatkit_python_sdk.base as base

@base.response_extractor
def create_role(chatkit_access_data, scope, name, permissions=[]):
    json_parameters = {
        "name": name,
        "scope": scope,
        "permissions": permissions
    }
    return base.chatkit_auth_request(chatkit_access_data, ["roles"], method="POST", json_parameters=json_parameters)

@base.response_extractor
def get_roles(chatkit_access_data):
    return base.chatkit_auth_request(chatkit_access_data, ["roles"], method="GET")

@base.response_extractor
def delete_role(chatkit_access_data, role_name, scope):
    endpoint_parts = ["roles", role_name, "scope", scope]
    return base.chatkit_auth_request(chatkit_access_data, endpoint_parts, method="DELETE")

@base.response_extractor
def set_user_role(chatkit_access_data, user_id, role_name, room_id=None):
    endpoint_parts = ["users", user_id, "roles"]

    json_parameters = {
        "name": role_name
    }

    if(room_id is not None):
        json_parameters['room_id'] = int(room_id)

    return base.chatkit_auth_request(chatkit_access_data, endpoint_parts, method="PUT", json_parameters=json_parameters)

@base.response_extractor
def get_user_roles(chatkit_access_data, user_id):

    endpoint_parts = ['users', user_id, "roles"]

    return base.chatkit_auth_request(chatkit_access_data, endpoint_parts, method="GET")

@base.response_extractor
def delete_user_role(chatkit_access_data, user_id, room_id=None):
    endpoint_parts = ['users', user_id, 'roles']

    query_parameters = {}

    if(room_id is not None):
        query_parameters["room_id"] = room_id

    return base.chatkit_auth_request(chatkit_access_data, endpoint_parts, query_parameters=query_parameters, method="DELETE")

@base.response_extractor
def get_role_permissions(chatkit_access_data, role_name, scope_name):
    endpoint_parts = ['roles', role_name, 'scope', scope_name, 'permissions']

    return base.chatkit_auth_request(chatkit_access_data, endpoint_parts, method="GET")

@base.response_extractor
def update_role_permissions(chatkit_access_data, role_name, scope_name, add_permissions=None, remove_permissions=None):
    endpoint_parts = ["roles", role_name, "scope", scope_name, "permissions"]

    permissions = {}

    if(add_permissions is not None):
        permissions['add_permissions'] = add_permissions

    if(remove_permissions is not None):
        permissions['remove_permissions'] = remove_permissions

    return base.chatkit_auth_request(chatkit_access_data, endpoint_parts, method="PUT", json_parameters=permissions)



