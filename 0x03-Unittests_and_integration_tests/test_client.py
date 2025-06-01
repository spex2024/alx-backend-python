#!/usr/bin/env python3
"""
Test module for the client.py functionality
"""

import unittest
from unittest.mock import patch, MagicMock
from fixtures import TEST_PAYLOAD
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @patch('client.get_json')
    def test_org(self, mock_get_json):
        """Test GithubOrgClient.org returns correct payload"""
        mock_get_json.return_value = TEST_PAYLOAD
        client = GithubOrgClient('google')
        self.assertEqual(client.org, TEST_PAYLOAD)
        mock_get_json.assert_called_once_with(
            'https://api.github.com/orgs/google'
        )

    def test_public_repos_url(self):
        """Test the _public_repos_url property"""
        client = GithubOrgClient('google')
        with patch.object(client, 'org', new_callable=MagicMock) as mock_org:
            mock_org.return_value = {'repos_url': 'https://api.github.com/orgs/google/repos'}
            self.assertEqual(client._public_repos_url, 'https://api.github.com/orgs/google/repos')

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method returns list of repo names"""
        mock_get_json.return_value = [
            {'name': 'repo1'}, {'name': 'repo2'}, {'name': 'repo3'}
        ]
        client = GithubOrgClient('google')
        with patch.object(client, '_public_repos_url',
                          new_callable=MagicMock) as mock_repos_url:
            mock_repos_url.return_value = 'mock_url'
            self.assertEqual(
                client.public_repos(),
                ['repo1', 'repo2', 'repo3']
            )
            mock_get_json.assert_called_once_with('mock_url')

    @patch('client.get_json')
    def test_has_license(self, mock_get_json):
        """Test has_license static method"""
        repo = {'license': {'key': 'mit'}}
        self.assertTrue(GithubOrgClient.has_license(repo, 'mit'))
        self.assertFalse(GithubOrgClient.has_license(repo, 'apache-2.0'))


if __name__ == '__main__':
    unittest.main()
