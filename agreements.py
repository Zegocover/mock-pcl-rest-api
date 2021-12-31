# coding: utf-8

import enum

import settings
from mock_data_handler import MockDataHandler


class AgreementsHandler:
    def __init__(self):
        self.cancellations_stage = 0
        self.defaults_stage = 0
        self.renewals_stage = 0
        self.cancellations_max_stage = 0
        self.defaults_max_stage = 0
        self.renewals_max_stage = 0
        self.mock_data_handler = MockDataHandler()

    class HeaderError(enum.Enum):
        NoHeaders = 'NoHeaders'
        InvalidDatetimeStamp = 'InvalidDatetimeStamp'
        InvalidClientOriginator = 'InvalidClientOriginator'
        InvalidClientChannel = 'InvalidClientChannel'
        InvalidClientChannelVersion = 'InvalidClientChannelVersion'
        InvalidRequestUID = 'InvalidRequestUID'
        InvalidAccessToken = 'InvalidAccessToken'
        InvalidSubscriptionKey = 'InvalidSubscriptionKey'
        InvalidContentType = 'InvalidContentType'
        InvalidRESTAPIVersion = 'InvalidRESTAPIVersion'

    HeaderErrorString = {
        HeaderError.NoHeaders: 'No any headers were found',
        HeaderError.InvalidDatetimeStamp: 'Invalid Date/Time Stamp',
        HeaderError.InvalidClientOriginator: 'Invalid pcl-apig-client-originator header',
        HeaderError.InvalidClientChannel: 'Invalid Pcl-Apig-Client-Channel header',
        HeaderError.InvalidClientChannelVersion: 'Invalid pcl-apig-client-channel-version header',
        HeaderError.InvalidRequestUID: 'Invalid pcl-apig-request-uid header',
        HeaderError.InvalidAccessToken: 'Invalid Authorization header',
        HeaderError.InvalidSubscriptionKey: 'Invalid Ocp-Apim-Subscription-Key header',
        HeaderError.InvalidContentType: 'Invalid Content-Type header',
        HeaderError.InvalidRESTAPIVersion: 'Invalid Api-Version header',
    }

    def _check_headers(self, headers):
        if not headers:
            return self.HeaderError.NoHeaders
        if 'pcl-apig-request-datetime-stamp' not in headers:
            return self.HeaderError.InvalidDatetimeStamp
        if 'pcl-apig-client-originator' not in headers or headers[
                'pcl-apig-client-originator'] != settings.PCL_APIG_CLIENT_ORIGINATOR:
            return self.HeaderError.InvalidClientOriginator
        if 'pcl-apig-client-channel' not in headers or headers[
                'pcl-apig-client-channel'] != settings.PCL_APIG_CLIENT_CHANNEL:
            return self.HeaderError.InvalidClientChannel
        if 'pcl-apig-client-channel-version' not in headers or headers[
                'pcl-apig-client-channel-version'] != settings.PCL_APIG_CLIENT_CHANNEL_VERSION:
            return self.HeaderError.InvalidClientChannelVersion
        if 'pcl-apig-request-uid' not in headers or headers['pcl-apig-request-uid'] != settings.PCL_APIG_REQUEST_UID:
            return self.HeaderError.InvalidRequestUID
        if 'Authorization' not in headers:
            return self.HeaderError.InvalidAccessToken
        if 'Ocp-Apim-Subscription-Key' not in headers or headers[
                'Ocp-Apim-Subscription-Key'] != settings.PCL_REST_API_SUBSCRIPTION_PRIMARY_KEY:
            return self.HeaderError.InvalidSubscriptionKey
        if 'Content-Type' not in headers or headers['Content-Type'] != 'application/json':
            return self.HeaderError.InvalidContentType
        if 'Api-Version' not in headers or headers['Api-Version'] != settings.PCL_REST_API_VERSION:
            return self.HeaderError.InvalidRESTAPIVersion
        return None

    @staticmethod
    def _handle_stage(stage, data):
        max_stage_num = len(data)
        if stage >= max_stage_num:
            stage = 0
        agreements_list = data[stage]['AgreementsList']
        stage += 1
        return stage, agreements_list

    def get_agreements(self, headers=None, params=None):
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

        if 'listName' not in params:
            res['errors'].append({
                'name': 'InvalidListName',
                'description': 'Wrong agreement list name.',
            })
            return res

        data = self.mock_data_handler.get_agreements_data()
        if params['listName'] == 'Defaults':
            self.defaults_stage, res['AgreementsList'] = self._handle_stage(self.defaults_stage,
                                                                            data['defaults_stages'])
        elif params['listName'] == 'Cancellations':
            self.cancellations_stage, res['AgreementsList'] = self._handle_stage(self.cancellations_stage,
                                                                                 data['cancellations_stages'])
        elif params['listName'] == 'Renewals':
            self.renewals_stage, res['AgreementsList'] = self._handle_stage(self.renewals_stage,
                                                                            data['renewals_stages'])
        return res
