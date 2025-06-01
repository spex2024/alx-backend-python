#!/usr/bin/env python3
"""
Test client module with parameterized_class and setup/teardown
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos"),
    [
        (
            TEST_PAYLOAD,
            [
                {"name": "repo1", "license": {"key": "mit"}},
                {"name": "repo2", "license": {"key": "apache-2.0"}},
                {"name": "repo3", "license": None},
                {"name": "repo4", "license": {"key": "mit"}},
            ],
            ["repo1", "repo2", "repo3", "repo4"],
        )
    ]
)
class TestGithubOrgClient(unittest.TestCase):
    """
    Test GithubOrgClient class
    """

    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_org(self):
        self.mock_get.return_value.json.return_value = self.org_payload
        client = GithubOrgClient('google')
        self.assertEqual(client.org, self.org_payload)
        self.mock_get.assert_called_once_with(
            'https://api.github.com/orgs/google'
        )

    def test_public_repos(self):
        client = GithubOrgClient('google')
        with patch.object(GithubOrgClient, 'org', new_callable=property) as mock_org:
            mock_org.return_value = {'repos_url': 'https://api.github.com/orgs/google/repos'}
            self.mock_get.return_value.json.return_value = self.repos_payload
            repos = client.public_repos()
            expected_names = [repo["name"] for repo in self.repos_payload]
            self.assertEqual(repos, expected_names)
            self.mock_get.assert_called_once_with(
                'https://api.github.com/orgs/google/repos'
            )

    def test_public_repos_with_license(self):
        client = GithubOrgClient('google')
        with patch.object(GithubOrgClient, 'org', new_callable=property) as mock_org:
            mock_org.return_value = {'repos_url': 'https://api.github.com/orgs/google/repos'}
            self.mock_get.return_value.json.return_value = self.repos_payload
            repos = client.public_repos(license_key='mit')
            filtered = [repo['name'] for repo in self.repos_payload if repo['license'] and repo['license']['key'] == 'mit']
            self.assertEqual(repos, filtered)
            self.mock_get.assert_called_once_with(
                'https://api.github.com/orgs/google/repos'
            )


if __name__ == '__main__':
    unittest.main()
