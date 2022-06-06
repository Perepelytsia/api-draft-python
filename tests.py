import unittest
import requests
import constants as c
from pytest_schema import schema
import json
import random


class TestPing(unittest.TestCase):

    def setUp(self):
        self.api_response = requests.get(c.API_APP_PING)

    def test_ping_status_code(self):
        self.assertEqual(self.api_response.status_code, c.STATUS_CODE_200)

    def test_ping_response_schema(self):
        self.assertEqual(schema(c.PING_RESPONSE_SCHEMA), json.loads(self.api_response.text))


class TestProfile(unittest.TestCase):

    def test_posts_missed_users(self):
        api_response = requests.get(c.API_APP_PROFILE)
        self.assertEqual(c.STATUS_CODE_400, api_response.status_code)
        self.assertEqual(c.ERR_MSG_USERS, json.loads(api_response.text))

if __name__ == '__main__':
    unittest.main()
