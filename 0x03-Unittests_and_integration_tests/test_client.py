#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient class."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns expected value and calls get_json once."""
        test_payload = {"org_name": org_name}
        mock_get_json.return_value = test_payload
        try:
            client = GithubOrgClient(org_name)
            self.assertEqual(client.org, test_payload)
            mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        except Exception as e:
            self.fail(f"Test failed with exception: {str(e)}")

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url returns expected repos_url."""
        test_payload = {"repos_url": "https://api.github.com/orgs/test/repos"}
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test")
            self.assertEqual(client._public_repos_url, test_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
    
