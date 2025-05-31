#!/usr/bin/env python3
"""Tests for client.py GithubOrgClient class."""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
import client  # assuming client.py is in same folder or package
import utils  # assuming utils.py is available similarly


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (
            {"login": "google"},
            [{"name": "repo1"}, {"name": "repo2"}],
            ["repo1", "repo2"],
            [{"name": "apache2_repo", "license": {"key": "apache-2.0"}}],
        )
    ],
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient.public_repos using fixtures."""

    @classmethod
    def setUpClass(cls):
        """Set up patcher for requests.get with side effects."""
        cls.get_patcher = patch("requests.get")
        cls.mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            if url.endswith(cls.org_payload["login"]):
                mock_resp = Mock()
                mock_resp.json.return_value = cls.org_payload
                return mock_resp
            elif url.endswith("/repos"):
                mock_resp = Mock()
                mock_resp.json.return_value = cls.repos_payload
                return mock_resp
            return Mock()

        cls.mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos list."""
        client_instance = client.GithubOrgClient(self.org_payload["login"])
        repos = client_instance.public_repos()
        self.assertEqual(repos, self.expected_repos)


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that org property returns correct value."""
        client_instance = client.GithubOrgClient(org_name)
        mock_get_json.return_value = {"org": org_name}
        result = client_instance.org
        self.assertEqual(result, {"org": org_name})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test the _public_repos_url property."""
        with patch.object(
            client.GithubOrgClient, "org", new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {"repos_url": "http://mocked.url/repos"}
            client_instance = client.GithubOrgClient("some_org")
            self.assertEqual(
                client_instance._public_repos_url,
                "http://mocked.url/repos"
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns list of repo names."""
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload
        with patch.object(
            client.GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos_url:
            mock_repos_url.return_value = "http://mocked.url/repos"
            client_instance = client.GithubOrgClient("org")
            repos = client_instance.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://mocked.url/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method with different licenses."""
        client_instance = client.GithubOrgClient("org")
        self.assertEqual(client_instance.has_license(repo, license_key), expected)
