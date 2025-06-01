#!/usr/bin/env python3
"""
Test the GithubOrgClient class with class-level parameterization
and patching requests.get.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized_class
from client import GithubOrgClient


@parameterized_class([
    {"org_name": "google"},
    {"org_name": "abc"}
])
class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient with parameterized org_name."""

    @classmethod
    def setUpClass(cls):
        # Patch requests.get for all tests in this class
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        cls.get_patcher.stop()

    def test_org(self):
        """Test that GithubOrgClient.org returns the correct value."""
        expected = {"login": self.org_name}
        # We simulate that requests.get().json() returns expected
        mock_response = self.mock_get.return_value
        mock_response.json.return_value = expected

        client = GithubOrgClient(self.org_name)
        self.assertEqual(client.org, expected)
        self.mock_get.assert_called_once_with(f"https://api.github.com/orgs/{self.org_name}")

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct value."""
        with patch("client.GithubOrgClient.org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": f"https://api.github.com/orgs/{self.org_name}/repos"}
            client = GithubOrgClient(self.org_name)
            self.assertEqual(client._public_repos_url, f"https://api.github.com/orgs/{self.org_name}/repos")

    def test_public_repos(self):
        """Test that public_repos returns the correct list of repo names."""
        repos_data = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_response = self.mock_get.return_value
        mock_response.json.return_value = repos_data

        with patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://some_url"
            client = GithubOrgClient(self.org_name)
            self.assertEqual(client.public_repos(), ["repo1", "repo2", "repo3"])
            self.mock_get.assert_called_once_with("http://some_url")

    def test_has_license(self):
        """Test has_license returns correct boolean based on repo license."""
        client = GithubOrgClient(self.org_name)

        repo_with_license = {"license": {"key": "my_license"}}
        self.assertTrue(client.has_license(repo_with_license, "my_license"))

        repo_with_other_license = {"license": {"key": "other_license"}}
        self.assertFalse(client.has_license(repo_with_other_license, "my_license"))


if __name__ == "__main__":
    unittest.main()
