# fixtures.py

TEST_PAYLOAD = [
    # 0: org_payload (dict)
    {
        "login": "google",
        "id": 1342004,
        "repos_url": "https://api.github.com/orgs/google/repos"
    },
    # 1: repos_payload (list of dicts)
    [
        {"name": "repo1", "license": {"key": "apache-2.0"}},
        {"name": "repo2", "license": {"key": "mit"}},
        {"name": "repo3", "license": {"key": "apache-2.0"}},
        {"name": "repo4", "license": None}
    ],
    # 2: expected_repos (list of all repo names)
    ["repo1", "repo2", "repo3", "repo4"],
    # 3: apache2_repos (list of repos with license key "apache-2.0")
    ["repo1", "repo3"]
]
