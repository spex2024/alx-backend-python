#!/usr/bin/env python3
"""
Test client module with parameterized_class and setup/teardown
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient  # Adjust import based on your project structure


@parameterized_class([
    {"org_payload": {"login": "google"}},
    {"org_payload": {"login": "abc"}}
])
class TestGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.patcher = patch('requests.get')
        cls.mock_get = cls.patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()

    def setUp(self):
        self.client = GithubOrgClient('google')

    def test_org(self):
        self.mock_get.return_value.json.return_value = self.org_payload
        result = self.client.org
        self.assertEqual(result, self.org_payload)
        self.mock_get.assert_called_once()

    def test_public_repos(self):
        repos_payload = [
            {'name': 'repo1', 'license': {'key': 'mit'}},
            {'name': 'repo2', 'license': None},
            {'name': 'repo3', 'license': {'key': 'apache-2.0'}}
        ]
        self.mock_get.return_value.json.return_value = repos_payload
        self.client._public_repos_url = 'http://fakeurl.com/repos'
        expected = ['repo1', 'repo2', 'repo3']
        result = self.client.public_repos()
        self.assertEqual(result, expected)

    def test_public_repos_with_license(self):
        repos_payload = [
            {'name': 'repo1', 'license': {'key': 'mit'}},
            {'name': 'repo2', 'license': None},
            {'name': 'repo3', 'license': {'key': 'apache-2.0'}}
        ]
        self.mock_get.return_value.json.return_value = repos_payload
        self.client._public_repos_url = 'http://fakeurl.com/repos'
        expected = ['repo1']
        result = self.client.public_repos(license_key='mit')
        self.assertEqual(result, expected)
