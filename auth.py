# coding: utf-8

import hashlib
import string
import random
import time
import enum

import settings


class AuthHandler:
    class HeaderError(enum.Enum):
        NoHeaders = 'NoHeaders'
        InvalidClientChannel = 'InvalidClientChannel'
        InvalidSubscriptionKey = 'InvalidSubscriptionKey'
        InvalidContentType = 'InvalidContentType'

    HeaderErrorString = {
        HeaderError.NoHeaders: 'No any headers were found',
        HeaderError.InvalidClientChannel: 'Invalid Pcl-Apig-Client-Channel header',
        HeaderError.InvalidSubscriptionKey: 'Invalid Ocp-Apim-Subscription-Key header',
        HeaderError.InvalidContentType: 'Invalid Content-Type header',
    }

    class ValueError(enum.Enum):
        NoValues = 'NoValues'
        InvalidClientSecret = 'InvalidClientSecret'
        InvalidClientID = 'InvalidClientID'
        InvalidGrantType = 'InvalidGrantType'

    ValueErrorString = {
        ValueError.NoValues: 'No any values found',
        ValueError.InvalidClientSecret: 'Invalid Client Secret value',
        ValueError.InvalidClientID: 'Invalid Client ID value',
        ValueError.InvalidGrantType: 'Invalid Grant Type value',
    }

    def _check_headers(self, headers):
        if not headers:
            return self.HeaderError.NoHeaders
        if 'Pcl-Apig-Client-Channel' not in headers or headers[
                'Pcl-Apig-Client-Channel'] != settings.PCL_APIG_CLIENT_CHANNEL:
            return self.HeaderError.InvalidClientChannel
        if 'Ocp-Apim-Subscription-Key' not in headers or headers[
                'Ocp-Apim-Subscription-Key'] != settings.PCL_REST_API_SUBSCRIPTION_PRIMARY_KEY:
            return self.HeaderError.InvalidSubscriptionKey
        if 'Content-Type' not in headers or headers['Content-Type'] != 'application/x-www-form-urlencoded':
            return self.HeaderError.InvalidContentType
        return None

    def _check_values(self, values):
        if not values:
            return self.ValueError.NoValues
        if 'client_secret' not in values or values['client_secret'] != settings.PCL_REST_API_CLIENT_SECRET:
            return self.ValueError.InvalidClientSecret
        if 'client_id' not in values or values['client_id'] != settings.PCL_REST_API_CLIENT_ID:
            return self.ValueError.InvalidClientID
        if 'grant_type' not in values or values['grant_type'] != 'client_credentials':
            return self.ValueError.InvalidGrantType
        return None

    def get_client_access_token(self, headers=None, values=None):
        res = {
            'errors': []
        }

        ch_res = self._check_headers(headers)
        if ch_res is not None:
            res['errors'].append({
                'name': ch_res.value,
                'description': self.HeaderErrorString[ch_res],
            })
            return res

        cv_res = self._check_values(values)
        if cv_res is not None:
            res['errors'].append({
                'name': cv_res.value,
                'description': self.ValueErrorString[cv_res],
            })
            return res

        length = random.randint(5, 12)
        letters = string.ascii_letters
        random_string = ''.join(random.choice(letters) for _ in range(length)).encode('utf-8')
        token = hashlib.sha256(random_string).hexdigest()
        res['token_type'] = 'Bearer'
        res['access_token'] = token
        res['expires_on'] = '{}'.format(int(time.time()) + 3600)
        return res
