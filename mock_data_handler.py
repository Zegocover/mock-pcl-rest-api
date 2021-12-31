# coding: utf-8

import json


class MockDataHandler:
    AGREEMENTS_DATA_FILENAME = 'agreements_mock_data.json'

    def get_agreements_data(self):
        data_file = open(self.AGREEMENTS_DATA_FILENAME, 'rb')
        data = json.load(data_file)
        return data
