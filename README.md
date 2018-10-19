# chatkit-python-sdk
A simple python interface to the Chatkit APIs.
The library is developed for python2.7, but should be easily adapted for python3.*

# Dependencies
* requests (tested with requests==2.13.0)
* jwt (tested with PyJWT==1.6.4)

# example usage

This is a simple example that shows how to build access tokens and how to use them

```python
import sys
sys.path.append("chatkit_python_sdk")

import chatkit_python_sdk.base
import chatkit_python_sdk.rooms
import chatkit_python_sdk.auth_flow

secret = "your secret"
instance = "your instance"

#Creating a superuser anon token
cad_su_anon = chatkit_python_sdk.base.ChatkitAccessData(secret, instance, superuser=True)

#Validating the token
af = chatkit_python_sdk.auth_flow.AuthFlow(secret, instance)
af.validate_token(cad_su_anon.access_token, chatkit_user_id=None, force_superuser=True)

#Calling the fetch_rooms API using the superuser access token
result = chatkit_python_sdk.rooms.fetch_rooms(cad_su_anon, include_private=True)

#Creating a user access token
cad_user = chatkit_python_sdk.base.ChatkitAccessData(secret, instance, user_id='the_chatkit_user_id')
af.validate_token(cad_user.access_token, chatkit_user_id='chatkit_user_id')