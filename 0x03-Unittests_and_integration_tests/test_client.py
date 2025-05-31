#!/usr/bin/env python3
"""Unittests for GithubOrgClient class"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
import client  # Your GithubOrgClient here
import fixtures  # Your fixtures.py with test data


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org() returns correct payload without executing get_json"""
        # Setup the mock to return a sample dictionary (it won't actually be called)
        mock_get_json.return_value = {"payload": True}

        client_instance = client.GithubOrgClient(org_name)
        result = client_instance.org()

        # Ensure get_json called once with correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        self.assertEqual(result, mock_get_json.return_value)

    def test_public_repos_url(self):
        """Test _public_repos_url property returns expected URL"""
        with patch.object(client.GithubOrgClient, "org",
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://fake-url.com"}
            client_instance = client.GithubOrgClient("any_org")
            self.assertEqual(client_instance._public_repos_url, "http://fake-url.com")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names"""
        # Mock _public_repos_url property
        with patch.object(client.GithubOrgClient, "_public_repos_url",
                          new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "http://fake-url.com"
            mock_get_json.return_value = [
                {"name": "repo1"},
                {"name": "repo2"},
            ]

            client_instance = client.GithubOrgClient("any_org")
            repos = client_instance.public_repos()

            self.assertEqual(repos, ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://fake-url.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        client_instance = client.GithubOrgClient("any_org")
        self.assertEqual(client_instance.has_license(repo, license_key), expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            fixtures.org_payload,
            fixtures.repos_payload,
            fixtures.expected_repos,
            fixtures.apache2_repos,
        )
    ],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and configure side effects for fixtures"""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def get_json_side_effect(url, *args, **kwargs):
            if url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                return cls.org_payload
            return None

        cls.mock_get.return_value.json.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns all repos from the fixture"""
        client_instance = client.GithubOrgClient(self.org_payload["login"])
        repos = client_instance.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter returns correct repos"""
        client_instance = client.GithubOrgClient(self.org_payload["login"])
        apache2_repos = client_instance.public_repos(license="apache-2.0")
        self.assertEqual(apache2_repos, self.apache2_repos)

    def test_get_patcher_is_requests_get(self):
        """Test that get_patcher is patching requests.get."""
        self.assertIn("requests.get", str(self.get_patcher))
