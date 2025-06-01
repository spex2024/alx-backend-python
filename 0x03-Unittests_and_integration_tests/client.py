#!/usr/bin/env python3
"""
Client module to interact with the GitHub API for organizations.
"""

import requests


def get_json(url):
    """Get JSON content from a URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


class GithubOrgClient:
    """GitHub organization client to fetch organization details and repos."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        """Initialize the client with the organization name."""
        self.org_name = org_name

    @property
    def org(self):
        """Return the JSON representation of the organization."""
        url = self.ORG_URL.format(self.org_name)
        return get_json(url)

    @property
    def _public_repos_url(self):
        """Return the URL to fetch the organization's public repositories."""
        return self.org.get("repos_url")

    def public_repos(self, license_key=None):
        """Return the list of public repository names.

        If license_key is provided, filter repos by that license key.

        Args:
            license_key (str, optional): The license key to filter repos by.

        Returns:
            list of str: List of repo names.
        """
        repos = get_json(self._public_repos_url)
        if license_key is None:
            return [repo["name"] for repo in repos]
        else:
            return [
                repo["name"]
                for repo in repos
                if repo.get("license") and repo["license"].get("key") == license_key
            ]

    def has_license(self, repo, license_key):
        """Check if a repo has a specific license key.

        Args:
            repo (dict): The repository dictionary.
            license_key (str): The license key to check.

        Returns:
            bool: True if the repo's license matches license_key, else False.
        """
        license_info = repo.get("license")
        if license_info is None:
            return False
        return license_info.get("key") == license_key
