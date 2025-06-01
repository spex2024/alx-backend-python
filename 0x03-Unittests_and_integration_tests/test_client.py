#!/usr/bin/env python3
"""
Test the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized_class


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        expected = {"login": org_name}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct value."""
        with patch(
            "client.GithubOrgClient.org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }
            client = GithubOrgClient("google")
            self.assertEqual(
                client._public_repos_url,
                "https://api.github.com/orgs/google/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repo names."""
        @parameterized_class([
            {
                "org_payload": {"login": "google", "repos_url": "https://api.github.com/orgs/google/repos"},
                "repos_payload": [
                    {"name": "repo1", "license": {"key": "my_license"}},
                    {"name": "repo2", "license": {"key": "other_license"}},
                    {"name": "repo3", "license": {"key": "my_license"}},
                ],
                "expected_repos": ["repo1", "repo2", "repo3"],
                "expected_repos_with_license": ["repo1", "repo3"],
                "org_name": "google"
            }
        ])
        class TestIntegrationGithubOrgClient(unittest.TestCase):
            """Integration tests for GithubOrgClient with parameterized_class."""

            @classmethod
            def setUpClass(cls):
                """Set up class-wide patchers."""
                cls.get_patcher = patch("requests.get")
                cls.mock_get = cls.get_patcher.start()

                # Mock org response
                org_response = unittest.mock.Mock()
                org_response.json.return_value = cls.org_payload
                # Mock repos response
                repos_response = unittest.mock.Mock()
                repos_response.json.return_value = cls.repos_payload

                # requests.get returns org_response first, then repos_response
                cls.mock_get.side_effect = [org_response, repos_response]

            @classmethod
            def tearDownClass(cls):
                """Stop patchers."""
                cls.get_patcher.stop()

            def test_public_repos(self):
                """Test public_repos returns all repo names."""
                client = GithubOrgClient(self.org_name)
                self.assertEqual(client.public_repos(), self.expected_repos)

            def test_public_repos_with_license(self):
                """Test public_repos returns only repos with given license."""
                client = GithubOrgClient(self.org_name)
                self.assertEqual(
                    client.public_repos(license="my_license"),
                    self.expected_repos_with_license
                )

            def test_get_patcher_is_requests_get(self):
                """Test that get_patcher is patching requests.get."""
                self.assertEqual(self.get_patcher.attribute, "get")
                self.assertEqual(self.get_patcher.get_original()[0].__module__, "requests")

            def test_public_repos_with_nonexistent_license(self):
                """Test public_repos returns empty list for nonexistent license."""
                client = GithubOrgClient(self.org_name)
                self.assertEqual(
                    client.public_repos(license="nonexistent_license"),
                    []
                )

            def test_public_repos_with_none_license(self):
                """Test public_repos returns all repos when license is None."""
                client = GithubOrgClient(self.org_name)
                self.assertEqual(
                    client.public_repos(license=None),
                    self.expected_repos
                )

            def test_org_payload_structure(self):
                """Test that org_payload has expected keys."""
                self.assertIn("login", self.org_payload)
                self.assertIn("repos_url", self.org_payload)

            def test_repos_payload_structure(self):
                """Test that each repo in repos_payload has expected keys."""
                for repo in self.repos_payload:
                    self.assertIn("name", repo)
                    self.assertIn("license", repo)
                    self.assertIn("key", repo["license"])
