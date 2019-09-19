from __future__ import annotations

import unittest
import uuid

import requests

from integration_tests.helpers import methods
from integration_tests.helpers.methods import get_asid


class MhsHttpRequestBuilder(object):
    """
    Responsible for building HTTP requests against the MHS service.
    """

    def __init__(self):
        self.headers = {}
        self.body = None
        self.assertor = unittest.TestCase('__init__')

    def with_headers(self, interaction_id: str, message_id: str, sync_async: bool) -> MhsHttpRequestBuilder:
        """
        Allows the setting of required headers for the MHS
        :param interaction_id: id of this interaction used within MHS to track this request lifecycle
        :param message_id: the message id
        :param sync_async: whether this request should execute synchronously or not
        :return: self
        """
        self.headers = {
            'Interaction-Id': interaction_id,
            'Message-Id': message_id,
            'Correlation-Id': str(uuid.uuid4()).upper(),
            'sync-async': str(sync_async),
            'from-asid': f'{get_asid()}'
        }

        return self

    def with_body(self, body) -> MhsHttpRequestBuilder:
        """
        Allows the setting of the payload for the HTTP request
        :param body: the payload to send
        :return: self
        """
        self.body = body

        return self

    def execute_post_expecting_success(self) -> MhsHttpRequestBuilder:
        """
        Execute a POST request against the MHS using the configured body and headers within this class.
        Asserts the response is successful.
        :return: self
        """
        response = requests.post(methods.get_mhs_hostname(), headers=self.headers, data=self.body)
        self.assertor.assertTrue(
            response.ok,
            f'A non successful error code was returned from server: {response.status_code}')

        return self