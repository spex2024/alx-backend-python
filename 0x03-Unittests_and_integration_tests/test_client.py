#!/usr/bin/env python3
"""
Test client module
"""

import unittest
from unittest.mock import patch, Mock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Test GithubOrgClient class
    """

    @patch('client.get_json', return_value=TEST_PAYLOAD)
    def test_org(self, mock_get_json):
        """
        Test org property returns correct payload
        """
        org_client = GithubOrgClient('google')
        self.assertEqual(org_client.org, TEST_PAYLOAD)
        mock_get_json.assert_called_once_with(
            'https://api.github.com/orgs/google'
        )

    @patch('client.get_json', return_value=TEST_PAYLOAD)
    def test_public_repos(self, mock_get_json):
        """
        Test public_repos method returns repository names
        """
        org_client = GithubOrgClient('google')
        with patch.object(GithubOrgClient, 'org', new_callable=property) as mock_org:
            mock_org.return_value = {'repos_url': 'https://api.github.com/orgs/google/repos'}
            mock_get_json.return_value = [
                {'name': 'repo1'},
                {'name': 'repo2'},
                {'name': 'repo3'}
            ]
            repos = org_client.public_repos()
            self.assertEqual(repos, ['repo1', 'repo2', 'repo3'])
            mock_get_json.assert_called_once_with(
                'https://api.github.com/orgs/google/repos'
            )

    @patch('client.get_json')
    def test_public_repos_with_license(self, mock_get_json):
        """
        Test public_repos with license filtering
        """
        mock_get_json.return_value = [
            {'name': 'repo1', 'license': {'key': 'mit'}},
            {'name': 'repo2', 'license': {'key': 'apache-2.0'}},
            {'name': 'repo3', 'license': None},
            {'name': 'repo4', 'license': {'key': 'mit'}}
        ]
        org_client = GithubOrgClient('google')
        with patch.object(GithubOrgClient, 'org', new_callable=property) as mock_org:
            mock_org.return_value = {'repos_url': 'https://api.github.com/orgs/google/repos'}
            repos = org_client.public_repos(license_key='mit')
            self.assertEqual(repos, ['repo1', 'repo4'])
            mock_get_json.assert_called_once_with(
                'https://api.github.com/orgs/google/repos'
            )


if __name__ == '__main__':
    unittest.main()
