#!/usr/bin/env python3
"""
Test module for the GithubOrgClient class.
Contains unit tests for GithubOrgClient methods including
org property, public_repos method, and license filtering.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org property returns the
        expected organization information from the API.
        """
        expected = {"login": org_name}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """
        Test that the _public_repos_url property returns the correct
        URL extracted from the org property.
        """
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/google/repos"}
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns a list of repository names
        from the URL specified by _public_repos_url.
        """
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://some_url"
            with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
                mock_org.return_value = {"repos_url": "http://some_url"}
                client = GithubOrgClient("google")
                self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])

        mock_get_json.assert_called_once_with("http://some_url")

    @patch("client.get_json")
    def test_public_repos_with_license(self, mock_get_json):
        """
        Test that public_repos filters repositories by license key correctly,
        returning only repo names that have the specified license.
        """
        repos = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}},
            {"name": "repo3", "license": {"key": "my_license"}},
        ]
        mock_get_json.return_value = repos

        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://some_url"
            with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
                mock_org.return_value = {"repos_url": "http://some_url"}
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
        Test the has_license method returns True if the
        repository's license matches the license_key, else False.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.has_license(repo, license_key), expected)


if __name__ == "__main__":
    unittest.main()
