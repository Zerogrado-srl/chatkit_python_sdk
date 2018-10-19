
import chatkit_python_sdk.base as base

class AuthorizationException(Exception):
    pass

class AuthFlow(object):

    def __init__(self, secret, instance):
        self.secret = secret
        self.instance = instance

    def create_chatkit_token(self, user_id):
        configuration = base.ChatkitAccessData(secret=self.secret, instance=self.instance, user_id=user_id)

        token = configuration.access_token
        expires_in = configuration.token_expires_in

        """
        access_token="your_token_here",
        user_id="hugh_mungus",
        token_type="access_token",
        expires_in="1504801895"
        """
        response = {
            "access_token": token,
            "user_id": user_id,
            "token_type": "access_token",
            "expires_in": expires_in
        }
        return response

    def validate_token(self, passed_token, chatkit_user_id, version='v1', region='us1', force_superuser=False):
        """
        Decodes the token, then uses the data to recompute it and then verifies that the recomputed one is equal to the passed one
        """

        key_id, key_secret = base.split_secret(self.secret)

        decoded_data = base.decode_token(passed_token, key_secret)

        instance = None
        expire_timestamp = None
        issue_timestamp = None
        user_id = None

        if(decoded_data is not None):
            expire_timestamp = decoded_data.get('exp', None)
            issue_timestamp = decoded_data.get('iat', None)
            #In token creation we do not use the whole instance locator string, but only the last part, otherwise the obtained token is not verified by ChatKit.
            #We should pass the whole string to ChatkitAccessData
            instance = version + ":" + region + ":" + decoded_data.get('instance', '')
            user_id = decoded_data.get('sub', None)
        else:
            raise AuthorizationException("Token validation failed")

        temp_cad = base.ChatkitAccessData(secret=self.secret, instance=self.instance, user_id=user_id, expire_timestamp=expire_timestamp, issue_timestamp=issue_timestamp, superuser=force_superuser)

        return temp_cad.verify_token(passed_token, chatkit_user_id)