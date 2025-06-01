# fixtures.py

TEST_PAYLOAD = [
    {"login": "google"},  # org_payload
    [                     # repos_payload
        {"name": "repo1", "license": {"key": "apache-2.0"}},
        {"name": "repo2", "license": {"key": "other"}},
    ],
    ["repo1", "repo2"],   # expected_repos
    ["repo1"]             # apache2_repos (filtered)
]
