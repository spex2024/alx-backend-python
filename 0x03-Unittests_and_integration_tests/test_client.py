#!/usr/bin/env python3
"""
Test module for the GithubOrgClient class.

Includes unit tests and integration tests for interacting with
the GitHub API to fetch organization and repository information.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns expected org data.
        """
        expected = {"login": org_name}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns repos_url from org property.
        """
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns a list of repo names.
        """
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://some_url"
            client = GithubOrgClient("google")
            self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
            mock_get_json.assert_called_once_with("http://some_url")

    @patch("client.get_json")
    def test_public_repos_with_license(self, mock_get_json):
        """
        Test that public_repos filters repos by license key.
        """
        repos = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}},
            {"name": "repo3", "license": {"key": "my_license"}},
        ]
        mock_get_json.return_value = repos
        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://some_url"
            client = GithubOrgClient("google")
            filtered = client.public_repos(license_key="my_license")
            self.assertEqual(filtered, ["repo1", "repo3"])
            mock_get_json.assert_called_once_with("http://some_url")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test has_license returns True if license matches, else False.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


@parameterized_class([
    {"org_payload": TEST_PAYLOAD[0],
     "repos_payload": TEST_PAYLOAD[1],
     "expected_repos": TEST_PAYLOAD[2],
     "apache2_repos": TEST_PAYLOAD[3]}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests using payloads from fixtures."""

    @classmethod
    def setUpClass(cls):
        """
        Patch requests.get and set up mock responses.
        """
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.return_value.json.side_effect = [
            cls.org_payload,
            cls.repos_payload,
            cls.org_payload,
            cls.repos_payload
        ]

    @classmethod
    def tearDownClass(cls):
        """
        Stop the requests.get patcher after all tests.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test public_repos returns all repo names.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test public_repos returns repos with license='apache-2.0'.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license_key="apache-2.0"), self.apache2_repos)


if __name__ == "__main__":
    unittest.main()
