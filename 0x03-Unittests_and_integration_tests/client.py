#!/usr/bin/env python3
"""GithubOrgClient module"""

import requests


def get_json(url):
    """Fetch JSON data from a URL"""
    return requests.get(url).json()


class GithubOrgClient:
    """Client to interact with GitHub organization."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Return organization info"""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self):
        """Return URL to the list of public repos"""
        return self.org.get("repos_url")

    def public_repos(self, license=None):
        """Return list of public repos (optionally filtered by license)"""
        repos = get_json(self._public_repos_url)
        if license is None:
            return [repo["name"] for repo in repos]
        return [
            repo["name"]
            for repo in repos
            if self.has_license(repo, license)
        ]

    @staticmethod
    def has_license(repo, license_key):
        """Check if a repo has a specific license"""
        try:
            return repo["license"]["key"] == license_key
        except Exception:
            return False
