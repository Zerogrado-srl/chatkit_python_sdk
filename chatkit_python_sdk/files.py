# coding=utf-8

import chatkit_python_sdk.base as base
import urllib2


def get_file(chatkit_access_data, room_id, file_name):
    endpoint_parts = ['rooms', room_id, 'fles', file_name]
    return base.chatkit_file_request(chatkit_access_data, endpoint_parts, method="GET")


def post_file(chatkit_access_data, room_id, user_id, file_name, source_local_file_path=None, source_url_file=None):
    endpoint_parts = ['rooms', room_id, 'users', user_id, 'files', file_name]

    file_parameters = {}

    if(source_local_file_path is not None):
        file_parameters['files'] = open(source_local_file_path, 'rb')

    elif(source_url_file is not None):
        try:
            remote_data_response = urllib2.urlopen(source_url_file)
            file_parameters['files'] = remote_data_response.read()
        except Exception, e:
            print("Eccezione in lettura remota file")
            raise e

    return base.chatkit_file_request(chatkit_access_data, endpoint_parts, method="POST", files=file_parameters)


def delete_file(chatkit_access_data, room_id, file_name):

    endpoint_parts = ['rooms', room_id, 'files', file_name]

    return base.chatkit_file_request(chatkit_access_data, endpoint_parts, method="DELETE")


def delete_all_user_files(chatkit_access_data, user_id):

    endpoint_parts = ['users', user_id]

    return base.chatkit_file_request(chatkit_access_data, endpoint_parts, method="DELETE")

