#!/usr/bin/env python3
"""
Test cases for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class
from client import GithubOrgClient


@parameterized_class([
    {"org_name": "google"},
    {"org_name": "abc"},
])
class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient behaviors."""

    @classmethod
    def setUpClass(cls):
        """Start patcher for client.get_json."""
        cls.get_patcher = patch("client.get_json")
        cls.mock_get_json = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop patcher for client.get_json."""
        cls.get_patcher.stop()


    def setUp(self):
        self.mock_get_json = type(self).mock_get_json

    def test_org(self):
        """Test that org property returns correct org data."""
        expected = {"login": self.org_name}
        self.mock_get_json.return_value = expected
        client = GithubOrgClient(self.org_name)
        self.assertEqual(client.org, expected)
        self.mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{self.org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the repos_url correctly."""
        with patch(
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": f"https://api.github.com/orgs/{self.org_name}/repos"
            }
            client = GithubOrgClient(self.org_name)
            self.assertEqual(
                client._public_repos_url,
                f"https://api.github.com/orgs/{self.org_name}/repos"
            )

    def test_public_repos(self):
        """Test that public_repos returns list of repo names."""
        repos_data = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        self.mock_get_json.return_value = repos_data

        with patch(
            "client.GithubOrgClient._public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://some_url"
            client = GithubOrgClient(self.org_name)
            self.assertEqual(
                client.public_repos(),
                ["repo1", "repo2", "repo3"]
            )
            self.mock_get_json.assert_called_once_with("http://some_url")
            mock_url.assert_called_once()

    def test_public_repos_with_license(self):
        """Test public_repos filters repos by license key correctly."""
        repos_data = [
            {"name": "repo1", "license": {"key": "my_license"}},
            {"name": "repo2", "license": {"key": "other_license"}},
            {"name": "repo3", "license": None},
        ]
        self.mock_get_json.return_value = repos_data

        with patch(
            "client.GithubOrgClient._public_repos_url", new_callable=PropertyMock
        ) as mock_url:
            mock_url.return_value = "http://some_url"
            client = GithubOrgClient(self.org_name)
            filtered = client.public_repos(license_key="my_license")
            self.assertEqual(filtered, ["repo1"])

    def test_has_license(self):
        """Test has_license returns True/False based on repo license."""
        client = GithubOrgClient(self.org_name)
        repo_with_license = {"license": {"key": "my_license"}}
        repo_with_other_license = {"license": {"key": "other_license"}}
        repo_with_no_license = {"license": None}

        self.assertTrue(client.has_license(repo_with_license, "my_license"))
        self.assertFalse(client.has_license(repo_with_other_license, "my_license"))
        self.assertFalse(client.has_license(repo_with_no_license, "my_license"))


if __name__ == "__main__":
    unittest.main()
