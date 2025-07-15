#!/usr/bin/env python3
"""Unit tests for client.GithubOrgClient class."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test case for GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('utils.get_json')
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


if __name__ == "__main__":
    unittest.main()
