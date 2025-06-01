import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import client
import requests
import fixtures
from utils import get_json

# !/usr/bin/env python3


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct value and get_json called once"""
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload
        client_obj = GithubOrgClient(org_name)
        self.assertEqual(client_obj.org, test_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns expected value from org payload"""
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            payload = {"repos_url": "http://some_url/repos"}
            mock_org.return_value = payload
            client_obj = GithubOrgClient("test")
            self.assertEqual(
                client_obj._public_repos_url, payload["repos_url"]
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list of repo names"""
        test_repos = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]
        mock_get_json.return_value = test_repos
        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://some_url/repos"
            client_obj = GithubOrgClient("test")
            result = client_obj.public_repos()
            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once_with("http://some_url/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct boolean"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)


@parameterized_class([
    {
        "org_payload": fixtures.org_payload,
        "repos_payload": fixtures.repos_payload,
        "expected_repos": fixtures.expected_repos,
        "apache2_repos": fixtures.apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up class: patch requests.get to return fixtures"""
        cls.get_patcher = patch('requests.get')
        mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url == GithubOrgClient.ORG_URL.format(org="google"):
                mock_resp.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = None
            return mock_resp

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repos"""
        client_obj = GithubOrgClient("google")
        self.assertEqual(client_obj.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos with license filter"""
        client_obj = GithubOrgClient("google")
        self.assertEqual(
            client_obj.public_repos(license="apache-2.0"),
            self.apache2_repos
        )

    def test_org_property_is_cached(self):
        """Test that org property is cached and requests.get is called only once"""
        client_obj = GithubOrgClient("google")
        org1 = client_obj.org
        org2 = client_obj.org
        self.assertIs(org1, org2)

    def test_public_repos_url_matches_org_payload(self):
        """Test that _public_repos_url matches repos_url in org_payload"""
        client_obj = GithubOrgClient("google")
        self.assertEqual(
            client_obj._public_repos_url, self.org_payload["repos_url"]
        )

    def test_public_repos_empty(self):
        """Test public_repos returns empty list if repos_payload is empty"""
        original_repos_payload = self.repos_payload
        self.repos_payload = []
        client_obj = GithubOrgClient("google")
        self.assertEqual(client_obj.public_repos(), [])
        self.repos_payload = original_repos_payload

    def test_public_repos_with_nonexistent_license(self):
        """Test public_repos returns empty list if no repo matches license"""
        client_obj = GithubOrgClient("google")
        self.assertEqual(
            client_obj.public_repos(license="nonexistent-license"), []
        )

    def test_has_license_true(self):
        """Test has_license returns True for matching license"""
        repo = {"license": {"key": "apache-2.0"}}
        self.assertTrue(GithubOrgClient.has_license(repo, "apache-2.0"))

    def test_has_license_false(self):
        """Test has_license returns False for non-matching license"""
        repo = {"license": {"key": "mit"}}
        self.assertFalse(GithubOrgClient.has_license(repo, "apache-2.0"))

    def test_has_license_no_license_key(self):
        """Test has_license returns False if license key is missing"""
        repo = {"license": {}}
        self.assertFalse(GithubOrgClient.has_license(repo, "apache-2.0"))

    def test_has_license_no_license(self):
        """Test has_license returns False if license is missing"""
        repo = {}
        self.assertFalse(GithubOrgClient.has_license(repo, "apache-2.0"))

    def test_org_payload_content(self):
        """Test that org payload contains expected keys"""
        client_obj = GithubOrgClient("google")
        org = client_obj.org
        self.assertIn("login", org)
        self.assertIn("repos_url", org)

    def test_repos_payload_content(self):
        """Test that repos payload contains expected repo names"""
        client_obj = GithubOrgClient("google")
        repos = client_obj.public_repos()
        for repo in self.expected_repos:
            self.assertIn(repo, repos)

    def test_public_repos_license_case_insensitive(self):
        """Test public_repos license filter is case sensitive"""
        client_obj = GithubOrgClient("google")
        # Should return empty if license key case does not match
        self.assertEqual(
            client_obj.public_repos(license="Apache-2.0"), []
        )

    def test_public_repos_with_none_license(self):
        """Test public_repos with license=None returns all repos"""
        client_obj = GithubOrgClient("google")
        self.assertEqual(
            client_obj.public_repos(license=None), self.expected_repos
        )

    def test_public_repos_with_missing_license_field(self):
        """Test public_repos skips repos with missing license field when filtering"""
        # Add a repo with no license field
        original_repos_payload = self.repos_payload
        self.repos_payload = self.repos_payload + [{"name": "repo_no_license"}]
        client_obj = GithubOrgClient("google")
        self.assertEqual(
            client_obj.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
        self.repos_payload = original_repos_payload

    def test_public_repos_with_empty_name(self):
        """Test public_repos skips repos with missing name field"""
        original_repos_payload = self.repos_payload
        self.repos_payload = self.repos_payload + [{"license": {"key": "apache-2.0"}}]
        client_obj = GithubOrgClient("google")
        repos = client_obj.public_repos()
        # Should not include None or missing names
        self.assertNotIn(None, repos)
        self.repos_payload = original_repos_payload


if __name__ == "__main__":
    unittest.main()