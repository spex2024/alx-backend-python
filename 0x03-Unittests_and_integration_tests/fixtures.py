#!/usr/bin/env python3
"""
Fixture module to provide test payloads.
"""

TEST_PAYLOAD = [
    {"login": "google"},
    [
        {"name": "repo1", "license": {"key": "apache-2.0"}},
        {"name": "repo2", "license": {"key": "apache-2.0"}},
        {"name": "repo3", "license": {"key": "mit"}},
    ],
    ["repo1", "repo2", "repo3"],
    ["repo1", "repo2"]  # only repos with apache-2.0 license
]
def get_test_payload():
    """Return the test payload for use in tests."""
    return TEST_PAYLOAD